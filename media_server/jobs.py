"""
jobs.py – helper layer for storing transcoding job metadata in SQLite
and deciding automatically whether we can do a zero-cost remux (H-264+AAC)
or must re-encode.

Features:
- In-memory progress cache for responsive UI without excessive DB writes
- Rich media info extraction: chapters, subtitles, HDR status, bitrate, frame rate
- Subtitle track detection with language and codec info
- Thumbnail metadata storage for seek previews
- Pydantic models for API responses with full type safety
"""
from __future__ import annotations

import json
import logging
import subprocess
import threading
import time
import uuid
from pathlib import Path
from typing import Optional, Tuple, Literal, List

from pydantic import BaseModel, Field, model_validator, field_validator

from media_server.config import cfg
from media_server.models import Job, db

# ─────────────────────────────────────────────────────────── logging
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────── in-memory progress cache

_progress_cache: dict[str, float] = {}
_progress_lock = threading.Lock()


def update_progress_memory(job_id: str, transcoded: float) -> None:
    """Update in-memory progress (fast, for UI polling)."""
    with _progress_lock:
        old_val = _progress_cache.get(job_id, 0.0)
        _progress_cache[job_id] = transcoded
        if transcoded - old_val > 10:  # Log every ~10 seconds of progress
            log.debug("[PROGRESS] [%s] memory cache updated: %.1f -> %.1f", job_id, old_val, transcoded)


def get_progress_memory(job_id: str) -> float | None:
    """Get cached progress, or None if not cached."""
    with _progress_lock:
        val = _progress_cache.get(job_id)
        if val is not None:
            log.debug("[PROGRESS] [%s] cache hit: %.1f", job_id, val)
        return val


def clear_progress_memory(job_id: str) -> None:
    """Remove job from progress cache (call when job completes)."""
    with _progress_lock:
        if job_id in _progress_cache:
            log.debug("[PROGRESS] [%s] clearing cache", job_id)
            _progress_cache.pop(job_id, None)


# ─────────────────────────────────────────────────────────── helpers (ffprobe)


def _ffprobe_json(path: Path, show_chapters: bool = False) -> dict:
    """
    Return the full ffprobe JSON (all streams + container format + optionally chapters).

    We *don't* use –select_streams because mixing several selectors in one
    flag (e.g. "v:0,a:0") is illegal and causes ffprobe to exit 1.
    """
    log.debug("[FFPROBE] probing: %s (chapters=%s)", path, show_chapters)
    try:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
        ]
        if show_chapters:
            cmd.append("-show_chapters")
        cmd.append(str(path))

        res = subprocess.run(cmd, check=True, text=True, capture_output=True)
        data = json.loads(res.stdout)
        stream_count = len(data.get("streams", []))
        chapter_count = len(data.get("chapters", []))
        log.debug("[FFPROBE] %s: found %d streams, %d chapters", path.name, stream_count, chapter_count)
        return data
    except subprocess.CalledProcessError as e:
        log.error("[FFPROBE] failed for %s: %s", path, e.stderr)
        raise
    except json.JSONDecodeError as e:
        log.error("[FFPROBE] invalid JSON for %s: %s", path, e)
        raise


def _ffprobe_duration(path: Path) -> float:
    log.debug("[FFPROBE] getting duration for: %s", path)
    info = _ffprobe_json(path)
    duration = float(info["format"]["duration"])
    log.debug("[FFPROBE] %s duration: %.2f seconds", path.name, duration)
    return duration


def _detect_media_type(path: Path) -> str:
    """Detect if file is audio or video based on extension and ffprobe."""
    log.debug("[DETECT] detecting media type for: %s", path)

    if path.suffix.lower() in cfg.AUDIO_EXTENSIONS:
        log.debug("[DETECT] %s: audio (by extension)", path.name)
        return "audio"

    info = _ffprobe_json(path)
    has_video = any(s["codec_type"] == "video" for s in info.get("streams", []))
    media_type = "video" if has_video else "audio"
    log.debug("[DETECT] %s: %s (by ffprobe)", path.name, media_type)
    return media_type


def _ffprobe_codecs_and_dims(path: Path) -> Tuple[str, str, int, int]:
    """
    Return (video_codec, audio_codec, width, height).

    Missing audio falls back to ``""``.
    """
    log.debug("[FFPROBE] getting codecs for: %s", path)
    info = _ffprobe_json(path)
    v_stream = next((s for s in info["streams"] if s["codec_type"] == "video"), {})
    a_stream = next((s for s in info["streams"] if s["codec_type"] == "audio"), {})

    vcodec = v_stream.get("codec_name", "")
    acodec = a_stream.get("codec_name", "")
    width = int(v_stream.get("width") or 0)
    height = int(v_stream.get("height") or 0)

    log.debug("[FFPROBE] %s: vcodec=%s, acodec=%s, dims=%dx%d",
              path.name, vcodec or "(none)", acodec or "(none)", width, height)
    return vcodec, acodec, width, height


def _extract_media_info(path: Path) -> dict:
    """
    Extract rich media information from a file using ffprobe.

    Returns a dict with: chapters, subtitles, audio_channels, video_bitrate,
    audio_bitrate, hdr, color_space, frame_rate, sample_rate, etc.
    """
    log.debug("[MEDIAINFO] extracting rich info for: %s", path)
    info = _ffprobe_json(path, show_chapters=True)

    result = {
        "chapters": [],
        "subtitles": [],
        "audio_channels": 0,
        "audio_codec": "",
        "video_codec": "",
        "video_bitrate": 0,
        "audio_bitrate": 0,
        "total_bitrate": 0,
        "width": 0,
        "height": 0,
        "frame_rate": 0.0,
        "sample_rate": 0,
        "hdr": False,
        "color_space": "",
        "color_transfer": "",
        "pixel_format": "",
    }

    # Extract format-level info
    fmt = info.get("format", {})
    if fmt.get("bit_rate"):
        try:
            result["total_bitrate"] = int(fmt["bit_rate"])
        except (ValueError, TypeError):
            pass

    # Extract chapters
    for ch in info.get("chapters", []):
        chapter = {
            "title": ch.get("tags", {}).get("title", ""),
            "start": float(ch.get("start_time", 0)),
            "end": float(ch.get("end_time", 0)),
        }
        result["chapters"].append(chapter)

    if result["chapters"]:
        log.debug("[MEDIAINFO] found %d chapters", len(result["chapters"]))

    # Process streams
    for stream in info.get("streams", []):
        codec_type = stream.get("codec_type", "")

        if codec_type == "video":
            result["video_codec"] = stream.get("codec_name", "")
            result["width"] = stream.get("width", 0)
            result["height"] = stream.get("height", 0)
            result["pixel_format"] = stream.get("pix_fmt", "")
            result["color_space"] = stream.get("color_space", "")
            result["color_transfer"] = stream.get("color_transfer", "")

            # Parse frame rate (e.g., "24000/1001" or "30/1")
            fr_str = stream.get("r_frame_rate", "0/1")
            try:
                num, den = map(int, fr_str.split("/"))
                if den > 0:
                    result["frame_rate"] = round(num / den, 3)
            except (ValueError, ZeroDivisionError):
                pass

            # Video bitrate
            if stream.get("bit_rate"):
                try:
                    result["video_bitrate"] = int(stream["bit_rate"])
                except (ValueError, TypeError):
                    pass

            # HDR detection based on color transfer
            hdr_transfers = {"smpte2084", "arib-std-b67", "smpte428", "bt2020-10", "bt2020-12"}
            if result["color_transfer"] in hdr_transfers:
                result["hdr"] = True
                log.debug("[MEDIAINFO] HDR detected: color_transfer=%s", result["color_transfer"])

            # Also check pixel format for HDR hints
            hdr_pix_fmts = {"yuv420p10le", "yuv420p10be", "yuv420p12le", "p010le", "p010be"}
            if result["pixel_format"] in hdr_pix_fmts:
                result["hdr"] = True

        elif codec_type == "audio":
            if not result["audio_codec"]:  # Take first audio stream
                result["audio_codec"] = stream.get("codec_name", "")
                result["audio_channels"] = stream.get("channels", 0)
                if stream.get("sample_rate"):
                    try:
                        result["sample_rate"] = int(stream["sample_rate"])
                    except (ValueError, TypeError):
                        pass
                if stream.get("bit_rate"):
                    try:
                        result["audio_bitrate"] = int(stream["bit_rate"])
                    except (ValueError, TypeError):
                        pass

        elif codec_type == "subtitle":
            sub_info = {
                "index": stream.get("index", 0),
                "codec": stream.get("codec_name", ""),
                "language": stream.get("tags", {}).get("language", "und"),
                "title": stream.get("tags", {}).get("title", ""),
                "forced": stream.get("disposition", {}).get("forced", 0) == 1,
                "default": stream.get("disposition", {}).get("default", 0) == 1,
            }
            result["subtitles"].append(sub_info)

    if result["subtitles"]:
        log.debug("[MEDIAINFO] found %d subtitle tracks", len(result["subtitles"]))

    log.debug("[MEDIAINFO] %s: %dx%d, %.2ffps, hdr=%s, %d subs, %d chapters",
              path.name, result["width"], result["height"], result["frame_rate"],
              result["hdr"], len(result["subtitles"]), len(result["chapters"]))

    return result


# ─────────────────────────────────────────────────────────── pydantic models


class ChapterInfo(BaseModel):
    """Chapter marker in a media file."""
    title: str = ""
    start: float = 0.0
    end: float = 0.0


class SubtitleInfo(BaseModel):
    """Embedded subtitle track information."""
    index: int = 0
    codec: str = ""
    language: str = "und"
    title: str = ""
    forced: bool = False
    default: bool = False
    file: Optional[str] = None  # Extracted VTT filename (set after extraction)
    url: Optional[str] = None   # URL path to extracted VTT (set after extraction)


class ThumbnailInfo(BaseModel):
    """Seek preview thumbnail information."""
    count: int = 0              # Number of thumbnails generated
    interval: int = 10          # Seconds between thumbnails
    width: int = 160            # Thumbnail width in pixels
    vtt_url: Optional[str] = None    # URL to WebVTT file with thumbnail timestamps
    thumbs_url: Optional[str] = None # Base URL for thumbnail images


class MediaInfo(BaseModel):
    """Rich media information extracted from source file."""
    chapters: List[ChapterInfo] = Field(default_factory=list)
    subtitles: List[SubtitleInfo] = Field(default_factory=list)
    thumbnails: Optional[ThumbnailInfo] = None  # Generated after transcode
    audio_channels: int = 0
    audio_codec: str = ""
    video_codec: str = ""
    video_bitrate: int = 0
    audio_bitrate: int = 0
    total_bitrate: int = 0
    width: int = 0
    height: int = 0
    frame_rate: float = 0.0
    sample_rate: int = 0
    hdr: bool = False
    color_space: str = ""
    color_transfer: str = ""
    pixel_format: str = ""


class TranscodeParams(BaseModel):
    """
    Parameters for a (re)-encoding job.

    Defaults: **copy** both streams → free remux.
    """

    media_type: Literal["video", "audio"] = Field("video")
    video_codec: str = Field("copy", pattern=r"^\w+$")
    audio_codec: str = Field("copy", pattern=r"^\w+$")
    width: Optional[int] = Field(None, gt=0)
    height: Optional[int] = Field(None, gt=0)
    vb: str = Field("0k", pattern=r"^\d+[kK]$")
    ab: str = Field("128k", pattern=r"^\d+[kK]$")
    preset: str = Field("fast", pattern=r"^\w+$")

    @field_validator("vb", "ab", mode="before")
    @classmethod
    def _norm_k(cls, v: str) -> str:
        return v.lower()

    @model_validator(mode="after")
    def _dims_required_when_encoding(self):
        if self.media_type == "video" and self.video_codec != "copy":
            if self.width is None or self.height is None:
                raise ValueError("width and height are required when transcoding video")
        return self


class JobInfo(BaseModel):
    """Pydantic model for API responses."""

    job_id: str
    src: str
    duration: float
    playlist_url: str
    started: float
    status: str
    transcoded: float
    params: TranscodeParams
    retry_count: int = 0
    media_info: Optional[MediaInfo] = None


# ─────────────────────────────────────────────────────────── db helpers


def _job_to_info(job: Job) -> JobInfo:
    """Convert Peewee Job model to Pydantic JobInfo."""
    # Parse media_info if present
    media_info = None
    if job.media_info_json and job.media_info_json != "{}":
        try:
            media_info = MediaInfo.model_validate_json(job.media_info_json)
        except Exception as e:
            log.warning("[DB] failed to parse media_info_json for %s: %s", job.job_id, e)

    return JobInfo(
        job_id=job.job_id,
        src=job.src,
        duration=job.duration,
        playlist_url=job.playlist_url,
        started=job.started,
        status=job.status,
        transcoded=job.transcoded,
        params=TranscodeParams.model_validate_json(job.params_json),
        retry_count=int(job.retry_count),
        media_info=media_info,
    )


def save_job(info: JobInfo) -> None:
    """Save or update a job in the database."""
    log.debug("[DB] save_job: %s (status=%s)", info.job_id, info.status)
    try:
        media_info_json = info.media_info.model_dump_json() if info.media_info else "{}"
        with db.connection_context():
            Job.insert(
                job_id=info.job_id,
                src=info.src,
                duration=info.duration,
                playlist_url=info.playlist_url,
                started=info.started,
                status=info.status,
                transcoded=info.transcoded,
                params_json=info.params.model_dump_json(),
                retry_count=info.retry_count,
                media_info_json=media_info_json,
            ).on_conflict(
                conflict_target=[Job.job_id],
                update={
                    Job.status: info.status,
                    Job.transcoded: info.transcoded,
                    Job.started: info.started,
                    Job.retry_count: info.retry_count,
                },
            ).execute()
        log.debug("[DB] save_job: %s saved successfully", info.job_id)
    except Exception as e:
        log.error("[DB] save_job failed for %s: %s", info.job_id, e, exc_info=True)
        raise


def load_job(job_id: str) -> Optional[JobInfo]:
    """Load a job from the database."""
    log.debug("[DB] load_job: %s", job_id)
    try:
        with db.connection_context():
            job = Job.get_or_none(Job.job_id == job_id)
            if job is None:
                log.debug("[DB] load_job: %s not found", job_id)
                return None
            info = _job_to_info(job)
            log.debug("[DB] load_job: %s found (status=%s)", job_id, info.status)
            return info
    except Exception as e:
        log.error("[DB] load_job failed for %s: %s", job_id, e, exc_info=True)
        raise


def update_job(job_id: str, **patch) -> JobInfo:
    """Update specific fields of a job."""
    log.debug("[DB] update_job: %s with %s", job_id, patch)
    try:
        with db.connection_context():
            job = Job.get_or_none(Job.job_id == job_id)
            if job is None:
                log.warning("[DB] update_job: %s not found", job_id)
                raise KeyError(job_id)

            for key, value in patch.items():
                setattr(job, key, value)
            job.save()

            info = _job_to_info(job)
            log.debug("[DB] update_job: %s updated (status=%s)", job_id, info.status)
            return info
    except KeyError:
        raise
    except Exception as e:
        log.error("[DB] update_job failed for %s: %s", job_id, e, exc_info=True)
        raise


# ─────────────────────────────────────────────────────────── public helpers


def generate_job_id(src_path: Path, params: TranscodeParams) -> str:
    """Deterministic UUID5 based on (mtime,size,params) – idempotent reuse."""
    st = src_path.stat()
    key_base = json.dumps(
        [st.st_mtime_ns, st.st_size, params.model_dump(mode="json")],
        sort_keys=True,
    )
    return uuid.uuid5(uuid.NAMESPACE_DNS, key_base).hex[:12]


def _auto_params_for_source(path: Path) -> TranscodeParams:
    """
    Decide whether we can remux or must transcode.

    For audio files: If AAC → passthrough, else transcode to AAC
    For video files: If H264+AAC → passthrough, else transcode
    """
    media_type = _detect_media_type(path)
    vcodec, acodec, w, h = _ffprobe_codecs_and_dims(path)

    if media_type == "audio":
        acodec_lower = (acodec or "").lower()
        if acodec_lower in {"aac", "mp4a"}:
            log.debug("source is AAC → remux")
            return TranscodeParams(media_type="audio", audio_codec="copy")
        else:
            return TranscodeParams(
                media_type="audio",
                audio_codec="aac",
                ab="192k",
            )

    # Video logic
    vcodec = (vcodec or "").lower()
    acodec = (acodec or "").lower()

    if vcodec in {"h264", "avc1"} and acodec.startswith("aac"):
        log.debug("source is H-264/AAC → remux")
        return TranscodeParams(media_type="video")

    if not w or not h:
        w, h = 1280, 720
    if w >= 1920:
        vb = "5000k"
    elif w >= 1280:
        vb = "2500k"
    else:
        vb = "1200k"
    return TranscodeParams(
        media_type="video",
        video_codec="libx264",
        audio_codec="aac",
        width=w,
        height=h,
        vb=vb,
        ab="128k",
        preset="fast",
    )


def enqueue_job(src_path: Path, params: Optional[TranscodeParams] = None) -> JobInfo:
    """
    Create (or reuse) a transcoding/remux job.

    If the caller supplied no params or both codecs are "copy",
    we probe the file and auto-select either passthrough or a safe
    libx264+aac profile.
    """
    log.debug("[ENQUEUE] enqueue_job called for: %s", src_path)
    log.debug("[ENQUEUE] provided params: %s", params.model_dump() if params else None)

    src_path = src_path.resolve()
    if not src_path.is_file():
        log.error("[ENQUEUE] file not found: %s", src_path)
        raise FileNotFoundError(src_path)

    file_size = src_path.stat().st_size
    log.debug("[ENQUEUE] file size: %.2f MB", file_size / 1024 / 1024)

    if params is None or (params.video_codec == "copy" and params.audio_codec == "copy"):
        log.debug("[ENQUEUE] auto-detecting optimal params...")
        params = _auto_params_for_source(src_path)
        log.debug("[ENQUEUE] auto params: %s", params.model_dump())

    job_id = generate_job_id(src_path, params)
    log.debug("[ENQUEUE] generated job_id: %s", job_id)

    existing = load_job(job_id)
    if existing and not existing.status.startswith("error"):
        log.info("[ENQUEUE] reusing existing job %s (status=%s)", job_id, existing.status)
        return existing

    if existing:
        log.debug("[ENQUEUE] found previous failed job %s, creating new", job_id)

    log.debug("[ENQUEUE] probing duration and media info...")
    duration = _ffprobe_duration(src_path)
    playlist = f"/media/{job_id}/playlist.m3u8"

    # Extract rich media info
    raw_media_info = _extract_media_info(src_path)
    media_info = MediaInfo(
        chapters=[ChapterInfo(**ch) for ch in raw_media_info.get("chapters", [])],
        subtitles=[SubtitleInfo(**sub) for sub in raw_media_info.get("subtitles", [])],
        audio_channels=raw_media_info.get("audio_channels", 0),
        audio_codec=raw_media_info.get("audio_codec", ""),
        video_codec=raw_media_info.get("video_codec", ""),
        video_bitrate=raw_media_info.get("video_bitrate", 0),
        audio_bitrate=raw_media_info.get("audio_bitrate", 0),
        total_bitrate=raw_media_info.get("total_bitrate", 0),
        width=raw_media_info.get("width", 0),
        height=raw_media_info.get("height", 0),
        frame_rate=raw_media_info.get("frame_rate", 0.0),
        sample_rate=raw_media_info.get("sample_rate", 0),
        hdr=raw_media_info.get("hdr", False),
        color_space=raw_media_info.get("color_space", ""),
        color_transfer=raw_media_info.get("color_transfer", ""),
        pixel_format=raw_media_info.get("pixel_format", ""),
    )

    info = JobInfo(
        job_id=job_id,
        src=str(src_path),
        duration=duration,
        playlist_url=playlist,
        started=time.time(),
        status="queued",
        transcoded=0.0,
        params=params,
        media_info=media_info,
    )

    log.debug("[ENQUEUE] saving job to database...")
    save_job(info)

    mode_str = f"{params.media_type} - "
    if params.media_type == "audio":
        mode_str += "copy" if params.audio_codec == "copy" else "transcode"
    else:
        mode_str += "copy" if params.video_codec == "copy" else "transcode"

    log.info(
        "🆕  [%s] queued %s (%.1fs, %.1fMB) – %s",
        job_id,
        src_path.name,
        duration,
        file_size / 1024 / 1024,
        mode_str,
    )
    return info


def update_extracted_subtitles(job_id: str, extracted: list[dict]) -> None:
    """
    Update job's media_info with extracted subtitle file paths.

    Called by worker after subtitle extraction completes.
    """
    if not extracted:
        return

    log.debug("[DB] updating extracted subtitles for job %s (%d subs)", job_id, len(extracted))

    try:
        with db.connection_context():
            job = Job.get_or_none(Job.job_id == job_id)
            if job is None:
                log.warning("[DB] update_extracted_subtitles: job %s not found", job_id)
                return

            # Parse existing media_info
            media_info_dict = {}
            if job.media_info_json and job.media_info_json != "{}":
                try:
                    media_info_dict = json.loads(job.media_info_json)
                except json.JSONDecodeError:
                    pass

            # Update subtitle entries with extracted file info
            subtitles = media_info_dict.get("subtitles", [])
            extracted_by_index = {e["index"]: e for e in extracted}

            for sub in subtitles:
                if sub.get("index") in extracted_by_index:
                    ext = extracted_by_index[sub["index"]]
                    sub["file"] = ext.get("file")
                    sub["url"] = ext.get("url")

            media_info_dict["subtitles"] = subtitles
            job.media_info_json = json.dumps(media_info_dict)
            job.save()

            log.debug("[DB] updated %d subtitle entries with extracted files", len(extracted))

    except Exception as e:
        log.error("[DB] update_extracted_subtitles failed for %s: %s", job_id, e, exc_info=True)


def update_thumbnails(job_id: str, thumbnail_info: dict) -> None:
    """
    Update job's media_info with generated thumbnail information.

    Called by worker after thumbnail generation completes.
    """
    if not thumbnail_info:
        return

    log.debug("[DB] updating thumbnails for job %s", job_id)

    try:
        with db.connection_context():
            job = Job.get_or_none(Job.job_id == job_id)
            if job is None:
                log.warning("[DB] update_thumbnails: job %s not found", job_id)
                return

            # Parse existing media_info
            media_info_dict = {}
            if job.media_info_json and job.media_info_json != "{}":
                try:
                    media_info_dict = json.loads(job.media_info_json)
                except json.JSONDecodeError:
                    pass

            # Add thumbnail info
            media_info_dict["thumbnails"] = thumbnail_info
            job.media_info_json = json.dumps(media_info_dict)
            job.save()

            log.debug("[DB] updated thumbnails for job %s (%d thumbs)",
                      job_id, thumbnail_info.get("count", 0))

    except Exception as e:
        log.error("[DB] update_thumbnails failed for %s: %s", job_id, e, exc_info=True)


def get_job(job_id: str) -> Optional[JobInfo]:
    """Get job info by ID, with live progress from memory cache."""
    log.debug("[GET_JOB] get_job: %s", job_id)
    info = load_job(job_id)
    if info is None:
        log.debug("[GET_JOB] %s not found", job_id)
        return None

    # Overlay in-memory progress if available (more recent than DB)
    cached_progress = get_progress_memory(job_id)
    if cached_progress is not None and cached_progress > info.transcoded:
        log.debug("[GET_JOB] %s: using cached progress %.1f (db was %.1f)",
                  job_id, cached_progress, info.transcoded)
        info = info.model_copy(update={"transcoded": cached_progress})

    return info


def list_jobs() -> list[JobInfo]:
    """List all jobs."""
    log.debug("[LIST_JOBS] listing all jobs")
    try:
        with db.connection_context():
            jobs = [_job_to_info(job) for job in Job.select()]
            log.debug("[LIST_JOBS] found %d jobs", len(jobs))
            return jobs
    except Exception as e:
        log.error("[LIST_JOBS] failed: %s", e, exc_info=True)
        raise

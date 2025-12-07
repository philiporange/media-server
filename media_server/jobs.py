"""
jobs.py – helper layer for storing transcoding job metadata in SQLite
and deciding automatically whether we can do a zero-cost remux (H-264+AAC)
or must re-encode.

Includes in-memory progress cache for responsive UI without excessive DB writes.
"""
from __future__ import annotations

import json
import logging
import subprocess
import threading
import time
import uuid
from pathlib import Path
from typing import Optional, Tuple, Literal

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
        _progress_cache[job_id] = transcoded


def get_progress_memory(job_id: str) -> float | None:
    """Get cached progress, or None if not cached."""
    with _progress_lock:
        return _progress_cache.get(job_id)


def clear_progress_memory(job_id: str) -> None:
    """Remove job from progress cache (call when job completes)."""
    with _progress_lock:
        _progress_cache.pop(job_id, None)


# ─────────────────────────────────────────────────────────── helpers (ffprobe)


def _ffprobe_json(path: Path) -> dict:
    """
    Return the full ffprobe JSON (all streams + container format).

    We *don't* use –select_streams because mixing several selectors in one
    flag (e.g. "v:0,a:0") is illegal and causes ffprobe to exit 1.
    """
    res = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(res.stdout)


def _ffprobe_duration(path: Path) -> float:
    info = _ffprobe_json(path)
    return float(info["format"]["duration"])


def _detect_media_type(path: Path) -> str:
    """Detect if file is audio or video based on extension and ffprobe."""
    if path.suffix.lower() in cfg.AUDIO_EXTENSIONS:
        return "audio"

    info = _ffprobe_json(path)
    has_video = any(s["codec_type"] == "video" for s in info.get("streams", []))
    return "video" if has_video else "audio"


def _ffprobe_codecs_and_dims(path: Path) -> Tuple[str, str, int, int]:
    """
    Return (video_codec, audio_codec, width, height).

    Missing audio falls back to ``""``.
    """
    info = _ffprobe_json(path)
    v_stream = next((s for s in info["streams"] if s["codec_type"] == "video"), {})
    a_stream = next((s for s in info["streams"] if s["codec_type"] == "audio"), {})

    vcodec = v_stream.get("codec_name", "")
    acodec = a_stream.get("codec_name", "")
    width = int(v_stream.get("width") or 0)
    height = int(v_stream.get("height") or 0)
    return vcodec, acodec, width, height


# ─────────────────────────────────────────────────────────── pydantic models


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


# ─────────────────────────────────────────────────────────── db helpers


def _job_to_info(job: Job) -> JobInfo:
    """Convert Peewee Job model to Pydantic JobInfo."""
    return JobInfo(
        job_id=job.job_id,
        src=job.src,
        duration=job.duration,
        playlist_url=job.playlist_url,
        started=job.started,
        status=job.status,
        transcoded=job.transcoded,
        params=TranscodeParams.model_validate_json(job.params_json),
    )


def save_job(info: JobInfo) -> None:
    """Save or update a job in the database."""
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
        ).on_conflict(
            conflict_target=[Job.job_id],
            update={
                Job.status: info.status,
                Job.transcoded: info.transcoded,
                Job.started: info.started,
            },
        ).execute()


def load_job(job_id: str) -> Optional[JobInfo]:
    """Load a job from the database."""
    with db.connection_context():
        job = Job.get_or_none(Job.job_id == job_id)
        if job is None:
            return None
        return _job_to_info(job)


def update_job(job_id: str, **patch) -> JobInfo:
    """Update specific fields of a job."""
    with db.connection_context():
        job = Job.get_or_none(Job.job_id == job_id)
        if job is None:
            raise KeyError(job_id)

        for key, value in patch.items():
            setattr(job, key, value)
        job.save()

        return _job_to_info(job)


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
    src_path = src_path.resolve()
    if not src_path.is_file():
        raise FileNotFoundError(src_path)

    if params is None or (params.video_codec == "copy" and params.audio_codec == "copy"):
        params = _auto_params_for_source(src_path)

    job_id = generate_job_id(src_path, params)
    existing = load_job(job_id)
    if existing and not existing.status.startswith("error"):
        return existing

    duration = _ffprobe_duration(src_path)
    playlist = f"/media/{job_id}/playlist.m3u8"

    info = JobInfo(
        job_id=job_id,
        src=str(src_path),
        duration=duration,
        playlist_url=playlist,
        started=time.time(),
        status="queued",
        transcoded=0.0,
        params=params,
    )
    save_job(info)

    mode_str = f"{params.media_type} - "
    if params.media_type == "audio":
        mode_str += "copy" if params.audio_codec == "copy" else "transcode"
    else:
        mode_str += "copy" if params.video_codec == "copy" else "transcode"

    log.info(
        "🆕  [%s] queued %s (%.1fs) – %s",
        job_id,
        src_path.name,
        duration,
        mode_str,
    )
    return info


def get_job(job_id: str) -> Optional[JobInfo]:
    """Get job info by ID, with live progress from memory cache."""
    info = load_job(job_id)
    if info is None:
        return None

    # Overlay in-memory progress if available (more recent than DB)
    cached_progress = get_progress_memory(job_id)
    if cached_progress is not None and cached_progress > info.transcoded:
        info = info.model_copy(update={"transcoded": cached_progress})

    return info


def list_jobs() -> list[JobInfo]:
    """List all jobs."""
    with db.connection_context():
        return [_job_to_info(job) for job in Job.select()]

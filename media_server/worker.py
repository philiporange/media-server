#!/usr/bin/env python3
"""
worker.py – background worker that polls the SQLite database for queued
transcode/remux jobs and runs ffmpeg to produce HLS output.

Features:
- FFmpeg validation at startup
- Hardware acceleration detection (NVENC, VAAPI, QSV) with automatic fallback
- Two-tier progress updates (memory: 1/sec, database: 1/30sec)
- Graceful shutdown on SIGTERM/SIGINT
- Periodic cleanup of old jobs
- Job cancellation support with direct process termination
- Zombie job recovery on startup
- Timeout watchdog for hung processes
- Automatic retry on transient failures
- Subtitle extraction to WebVTT from embedded text-based subtitles
- Seek preview thumbnail generation at configurable intervals
"""
from __future__ import annotations

import json
import logging
import signal
import shutil
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path

from media_server.config import cfg
from media_server import jobs
from media_server.models import Job, claim_next_queued_job, recover_stale_jobs, cleanup_old_jobs

# Logging
LOG_LVL = logging.getLevelName(
    (logging.getLogger().level if logging.getLogger().handlers else 0) or "INFO"
)
logging.basicConfig(level=LOG_LVL, format="%(asctime)s %(levelname)-8s %(message)s")
log = logging.getLogger(__name__)

# Timing constants
POLL_INTERVAL = 0.5          # seconds between queue checks
MEMORY_UPDATE_INTERVAL = 1.0  # in-memory progress update frequency
DB_UPDATE_INTERVAL = 30.0     # database progress persist frequency
CLEANUP_INTERVAL = 3600       # hourly cleanup
CANCEL_CHECK_INTERVAL = 2.0   # how often to check for cancellation

# Graceful shutdown
_shutdown_requested = False

# Process tracking for direct termination on cancel
_active_processes: dict[str, subprocess.Popen] = {}
_process_lock = threading.Lock()

# Hardware acceleration detection cache
_hw_accel_encoder: str | None = None  # Detected encoder (e.g., "h264_nvenc")
_hw_accel_type: str | None = None     # Type: "nvenc", "vaapi", "qsv", or None


def _handle_shutdown(signum, frame):
    global _shutdown_requested
    log.info("shutdown requested (signal %d), finishing current jobs...", signum)
    _shutdown_requested = True


def _validate_ffmpeg() -> bool:
    """
    Verify ffmpeg and ffprobe are available and functional.

    Returns True if validation passes, False otherwise.
    """
    log.debug("[FFMPEG] validating ffmpeg installation")
    for cmd in ["ffmpeg", "ffprobe"]:
        log.debug("[FFMPEG] checking %s...", cmd)
        try:
            result = subprocess.run(
                [cmd, "-version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                log.error("[FFMPEG] %s returned non-zero exit code: %d", cmd, result.returncode)
                log.debug("[FFMPEG] %s stderr: %s", cmd, result.stderr)
                return False
            # Extract version from first line
            version = result.stdout.split('\n')[0] if result.stdout else "unknown"
            log.debug("[FFMPEG] %s version: %s", cmd, version)
        except FileNotFoundError:
            log.error("[FFMPEG] %s not found in PATH", cmd)
            return False
        except subprocess.TimeoutExpired:
            log.error("[FFMPEG] %s -version timed out after 10s", cmd)
            return False
        except Exception as e:
            log.error("[FFMPEG] %s validation failed: %s", cmd, e, exc_info=True)
            return False
    log.debug("[FFMPEG] validation complete - all tools available")
    return True


def _detect_hw_accel() -> tuple[str | None, str | None]:
    """
    Detect available hardware acceleration encoders.

    Tests NVENC, VAAPI, and QSV in order of preference.
    Returns (encoder_name, accel_type) or (None, None) if none available.
    """
    global _hw_accel_encoder, _hw_accel_type

    # Check config setting
    if cfg.HW_ACCEL == "none":
        log.info("[HW_ACCEL] disabled by configuration")
        return None, None

    # Hardware encoder configurations: (encoder, accel_type, test_args)
    hw_configs = [
        # NVIDIA NVENC
        ("h264_nvenc", "nvenc", ["-f", "lavfi", "-i", "nullsrc=s=256x256:d=1", "-c:v", "h264_nvenc", "-f", "null", "-"]),
        # Intel/AMD VAAPI (Linux)
        ("h264_vaapi", "vaapi", ["-init_hw_device", "vaapi=va:/dev/dri/renderD128", "-f", "lavfi", "-i", "nullsrc=s=256x256:d=1", "-vf", "format=nv12,hwupload", "-c:v", "h264_vaapi", "-f", "null", "-"]),
        # Intel QSV
        ("h264_qsv", "qsv", ["-init_hw_device", "qsv=qsv:MFX_IMPL_hw", "-f", "lavfi", "-i", "nullsrc=s=256x256:d=1", "-c:v", "h264_qsv", "-f", "null", "-"]),
    ]

    # If specific acceleration is requested, filter to just that
    if cfg.HW_ACCEL in ("nvenc", "vaapi", "qsv"):
        hw_configs = [(e, t, a) for e, t, a in hw_configs if t == cfg.HW_ACCEL]
        log.debug("[HW_ACCEL] testing only %s (configured)", cfg.HW_ACCEL)

    for encoder, accel_type, test_args in hw_configs:
        log.debug("[HW_ACCEL] testing %s (%s)...", encoder, accel_type)
        try:
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error"] + test_args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                log.info("[HW_ACCEL] detected %s (%s)", encoder, accel_type)
                _hw_accel_encoder = encoder
                _hw_accel_type = accel_type
                return encoder, accel_type
            else:
                log.debug("[HW_ACCEL] %s not available: %s", encoder, result.stderr.strip()[:100])
        except subprocess.TimeoutExpired:
            log.debug("[HW_ACCEL] %s test timed out", encoder)
        except Exception as e:
            log.debug("[HW_ACCEL] %s test failed: %s", encoder, e)

    log.info("[HW_ACCEL] no hardware acceleration available, using software encoding")
    return None, None


def get_hw_encoder() -> str | None:
    """Get the detected hardware encoder, or None if not available."""
    return _hw_accel_encoder


def get_hw_accel_type() -> str | None:
    """Get the detected hardware acceleration type."""
    return _hw_accel_type


# Text-based subtitle codecs that can be converted to WebVTT
TEXT_SUBTITLE_CODECS = {"subrip", "srt", "ass", "ssa", "mov_text", "webvtt", "text"}


def _generate_thumbnails(job_id: str, src: Path, out_dir: Path, duration: float) -> dict | None:
    """
    Generate seek preview thumbnails at regular intervals.

    Creates individual thumbnail images and a WebVTT file for thumbnail previews.
    Returns dict with thumbnail info or None if generation fails/disabled.
    """
    if not cfg.GENERATE_THUMBNAILS:
        log.debug("[THUMBNAILS] [%s] generation disabled", job_id)
        return None

    if duration <= 0:
        log.debug("[THUMBNAILS] [%s] skipping (invalid duration)", job_id)
        return None

    interval = cfg.THUMBNAIL_INTERVAL
    width = cfg.THUMBNAIL_WIDTH
    thumb_count = max(1, int(duration / interval))

    log.info("[THUMBNAILS] [%s] generating %d thumbnails (every %ds)", job_id, thumb_count, interval)

    thumbs_dir = out_dir / "thumbs"
    thumbs_dir.mkdir(exist_ok=True)

    # Use ffmpeg to extract thumbnails at regular intervals
    # fps=1/{interval} extracts one frame every {interval} seconds
    thumb_pattern = str(thumbs_dir / "thumb_%04d.jpg")

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-i", str(src),
        "-vf", f"fps=1/{interval},scale={width}:-1",
        "-q:v", "5",  # JPEG quality (2-31, lower is better)
        thumb_pattern,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=max(120, int(duration / 10)),  # Scale timeout with duration
        )

        if result.returncode != 0:
            log.warning("[THUMBNAILS] [%s] ffmpeg failed: %s", job_id, result.stderr.strip()[:200])
            return None

        # Count generated thumbnails
        thumb_files = sorted(thumbs_dir.glob("thumb_*.jpg"))
        if not thumb_files:
            log.warning("[THUMBNAILS] [%s] no thumbnails generated", job_id)
            return None

        log.debug("[THUMBNAILS] [%s] generated %d thumbnail files", job_id, len(thumb_files))

        # Generate WebVTT file for thumbnail sprite
        vtt_path = out_dir / "thumbnails.vtt"
        with open(vtt_path, "w") as f:
            f.write("WEBVTT\n\n")

            for i, thumb_file in enumerate(thumb_files):
                start_time = i * interval
                end_time = min((i + 1) * interval, duration)

                # Format timestamps as HH:MM:SS.mmm
                start_str = _format_vtt_time(start_time)
                end_str = _format_vtt_time(end_time)

                # Relative URL to thumbnail
                thumb_url = f"thumbs/{thumb_file.name}"

                f.write(f"{start_str} --> {end_str}\n")
                f.write(f"{thumb_url}\n\n")

        log.info("[THUMBNAILS] [%s] generated %d thumbnails + VTT", job_id, len(thumb_files))

        return {
            "count": len(thumb_files),
            "interval": interval,
            "width": width,
            "vtt_url": f"/media/{job_id}/thumbnails.vtt",
            "thumbs_url": f"/media/{job_id}/thumbs/",
        }

    except subprocess.TimeoutExpired:
        log.warning("[THUMBNAILS] [%s] timeout generating thumbnails", job_id)
        return None
    except Exception as e:
        log.warning("[THUMBNAILS] [%s] error: %s", job_id, e)
        return None


def _format_vtt_time(seconds: float) -> str:
    """Format seconds as VTT timestamp (HH:MM:SS.mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def _extract_subtitles(job_id: str, src: Path, out_dir: Path, subtitles: list[dict]) -> list[dict]:
    """
    Extract embedded text subtitles to WebVTT format.

    Returns list of extracted subtitle info with file paths.
    Image-based subtitles (PGS, VobSub) are skipped as they require OCR.
    """
    if not cfg.EXTRACT_SUBTITLES:
        log.debug("[SUBTITLES] [%s] extraction disabled", job_id)
        return []

    if not subtitles:
        log.debug("[SUBTITLES] [%s] no subtitles to extract", job_id)
        return []

    extracted = []

    for sub in subtitles:
        codec = sub.get("codec", "").lower()
        index = sub.get("index", 0)
        lang = sub.get("language", "und")
        title = sub.get("title", "")

        # Skip image-based subtitles
        if codec not in TEXT_SUBTITLE_CODECS:
            log.debug("[SUBTITLES] [%s] skipping image-based subtitle %d (%s)",
                      job_id, index, codec)
            continue

        # Generate output filename
        label = title or lang
        safe_label = "".join(c if c.isalnum() or c in "-_" else "_" for c in label)
        vtt_filename = f"sub_{index}_{safe_label}.vtt"
        vtt_path = out_dir / vtt_filename

        log.debug("[SUBTITLES] [%s] extracting subtitle %d (%s) to %s",
                  job_id, index, codec, vtt_filename)

        try:
            cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-y",
                "-i", str(src),
                "-map", f"0:{index}",
                "-c:s", "webvtt",
                str(vtt_path),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0 and vtt_path.exists():
                extracted.append({
                    "index": index,
                    "language": lang,
                    "title": title,
                    "codec": codec,
                    "file": vtt_filename,
                    "url": f"/media/{job_id}/{vtt_filename}",
                })
                log.info("[SUBTITLES] [%s] extracted %s (%s)", job_id, vtt_filename, lang)
            else:
                log.warning("[SUBTITLES] [%s] failed to extract subtitle %d: %s",
                            job_id, index, result.stderr.strip()[:200])

        except subprocess.TimeoutExpired:
            log.warning("[SUBTITLES] [%s] timeout extracting subtitle %d", job_id, index)
        except Exception as e:
            log.warning("[SUBTITLES] [%s] error extracting subtitle %d: %s", job_id, index, e)

    if extracted:
        log.info("[SUBTITLES] [%s] extracted %d/%d subtitles",
                 job_id, len(extracted), len(subtitles))

    return extracted


def register_process(job_id: str, proc: subprocess.Popen) -> None:
    """Register an active ffmpeg process for potential cancellation."""
    with _process_lock:
        _active_processes[job_id] = proc
        log.debug("[PROCESS] registered process for job %s (pid=%d, total=%d)",
                  job_id, proc.pid, len(_active_processes))


def unregister_process(job_id: str) -> None:
    """Remove a process from the active tracking dict."""
    with _process_lock:
        if job_id in _active_processes:
            _active_processes.pop(job_id)
            log.debug("[PROCESS] unregistered process for job %s (remaining=%d)",
                      job_id, len(_active_processes))


def terminate_process(job_id: str) -> bool:
    """
    Terminate the ffmpeg process for a job if it's running.

    Returns True if a process was terminated, False if no process found.
    """
    with _process_lock:
        proc = _active_processes.get(job_id)
        if proc and proc.poll() is None:
            log.info("[PROCESS] terminating process for job %s (pid=%d)", job_id, proc.pid)
            proc.terminate()
            return True
        elif proc:
            log.debug("[PROCESS] process for job %s already exited (rc=%s)", job_id, proc.poll())
        else:
            log.debug("[PROCESS] no process found for job %s", job_id)
    return False


def _run_ffmpeg(job_id: str, src: Path, p: jobs.TranscodeParams) -> str:
    """
    Execute one ffmpeg process with two-tier progress updates.

    - In-memory updates: every 1 second (for responsive UI)
    - Database persistence: every 30 seconds (reduces I/O)
    - Cancellation checks: every 2 seconds
    - Timeout watchdog: kills process if no output for FFMPEG_TIMEOUT seconds

    Returns: "done", "cancelled", "timeout", or "error:{code}"
    """
    out_dir = cfg.HLS_DIR / job_id
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    seg_pattern = str(out_dir / "%d.ts")

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-y",
        "-i",
        str(src),
    ]

    segment_duration = cfg.AUDIO_SEGMENT_DURATION if p.media_type == "audio" else cfg.SEGMENT_DURATION

    if p.media_type == "audio":
        cmd += ["-vn"]

        if p.audio_codec == "copy":
            cmd += ["-c:a", "copy"]
        else:
            cmd += [
                "-c:a",
                p.audio_codec,
                "-b:a",
                p.ab,
                "-ar",
                "44100",
                "-ac",
                "2",
            ]
    else:
        if p.video_codec == "copy":
            cmd += ["-c:v", "copy"]
        else:
            gop = segment_duration * 25
            bufsize = f"{2 * int(p.vb.rstrip('k'))}k"

            # Determine encoder to use (hardware or software)
            hw_encoder = get_hw_encoder()
            hw_type = get_hw_accel_type()
            use_hw = hw_encoder and p.video_codec == "libx264"

            if use_hw and hw_type == "nvenc":
                # NVIDIA NVENC encoding
                vf = (
                    f"scale={p.width}:{p.height}:force_original_aspect_ratio=decrease,"
                    f"pad={p.width}:{p.height}:(ow-iw)/2:(oh-ih)/2"
                )
                cmd += [
                    "-vf", vf,
                    "-c:v", "h264_nvenc",
                    "-b:v", p.vb,
                    "-maxrate", p.vb,
                    "-bufsize", bufsize,
                    "-g", str(gop),
                    "-preset", "p4",  # NVENC preset (p1=fastest, p7=slowest)
                    "-rc", "vbr",
                ]
                log.debug("[FFMPEG] [%s] using NVENC hardware encoding", job_id)

            elif use_hw and hw_type == "vaapi":
                # VAAPI encoding (Intel/AMD on Linux)
                cmd.insert(1, "-vaapi_device")
                cmd.insert(2, "/dev/dri/renderD128")
                vf = (
                    f"format=nv12,hwupload,"
                    f"scale_vaapi=w={p.width}:h={p.height}:force_original_aspect_ratio=decrease"
                )
                cmd += [
                    "-vf", vf,
                    "-c:v", "h264_vaapi",
                    "-b:v", p.vb,
                    "-maxrate", p.vb,
                    "-bufsize", bufsize,
                    "-g", str(gop),
                ]
                log.debug("[FFMPEG] [%s] using VAAPI hardware encoding", job_id)

            elif use_hw and hw_type == "qsv":
                # Intel QSV encoding
                cmd.insert(1, "-init_hw_device")
                cmd.insert(2, "qsv=qsv:MFX_IMPL_hw")
                cmd.insert(3, "-filter_hw_device")
                cmd.insert(4, "qsv")
                vf = (
                    f"format=nv12,hwupload=extra_hw_frames=64,"
                    f"scale_qsv=w={p.width}:h={p.height}"
                )
                cmd += [
                    "-vf", vf,
                    "-c:v", "h264_qsv",
                    "-b:v", p.vb,
                    "-maxrate", p.vb,
                    "-bufsize", bufsize,
                    "-g", str(gop),
                    "-preset", "faster",
                ]
                log.debug("[FFMPEG] [%s] using QSV hardware encoding", job_id)

            else:
                # Software encoding (libx264)
                vf = (
                    f"scale={p.width}:{p.height}:force_original_aspect_ratio=decrease,"
                    f"pad={p.width}:{p.height}:(ow-iw)/2:(oh-ih)/2"
                )
                cmd += [
                    "-vf", vf,
                    "-c:v", p.video_codec,
                    "-b:v", p.vb,
                    "-maxrate", p.vb,
                    "-bufsize", bufsize,
                    "-g", str(gop),
                    "-keyint_min", str(gop),
                    "-sc_threshold", "0",
                    "-preset", p.preset,
                ]

        if p.audio_codec == "copy":
            cmd += ["-c:a", "copy"]
        else:
            cmd += [
                "-c:a",
                p.audio_codec,
                "-b:a",
                p.ab,
                "-ar",
                "44100",
                "-ac",
                "2",
            ]

    cmd += [
        "-f",
        "hls",
        "-hls_time",
        str(segment_duration),
        "-hls_list_size",
        "0",
        "-hls_segment_type",
        "mpegts",
        "-hls_playlist_type",
        "event",
        "-hls_flags",
        "independent_segments+append_list+program_date_time+temp_file",
        "-hls_segment_filename",
        seg_pattern,
        "-max_muxing_queue_size",
        "1024",
        str(out_dir / "playlist.m3u8"),
        "-progress",
        "pipe:1",
    ]

    mode_str = f"{p.media_type} - "
    if p.media_type == "audio":
        mode_str += "copy" if p.audio_codec == "copy" else "transcode"
    else:
        mode_str += "copy" if p.video_codec == "copy" else "transcode"

    log.info("▶️  [%s] ffmpeg start (%s)", job_id, mode_str)
    log.debug("[FFMPEG] [%s] source: %s", job_id, src)
    log.debug("[FFMPEG] [%s] output dir: %s", job_id, out_dir)
    log.debug("[FFMPEG] [%s] params: media_type=%s, v_codec=%s, a_codec=%s, preset=%s",
              job_id, p.media_type, p.video_codec, p.audio_codec, p.preset)
    log.debug("[FFMPEG] [%s] command: %s", job_id, ' '.join(cmd))

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log.debug("[FFMPEG] [%s] process started (pid=%d)", job_id, proc.pid)

    # Register process for direct termination on cancel
    register_process(job_id, proc)

    last_time_sec = 0.0
    last_memory_update = 0.0
    last_db_update = 0.0
    last_cancel_check = 0.0
    last_output_time = time.time()  # For timeout watchdog
    cancelled = False
    timed_out = False
    result_status = "done"

    try:
        if proc.stdout is None:
            raise RuntimeError("ffmpeg stdout pipe missing")

        for ln in proc.stdout:
            now = time.time()
            last_output_time = now  # Reset watchdog timer on any output

            if "out_time_ms=" in ln:
                try:
                    ms = int(ln.strip().split("=", 1)[1])
                    last_time_sec = ms / 1_000_000

                    # High-frequency in-memory updates (for responsive UI)
                    if now - last_memory_update >= MEMORY_UPDATE_INTERVAL:
                        jobs.update_progress_memory(job_id, last_time_sec)
                        last_memory_update = now

                    # Low-frequency database persistence
                    if now - last_db_update >= DB_UPDATE_INTERVAL:
                        jobs.update_job(job_id, transcoded=last_time_sec)
                        last_db_update = now

                    # Periodic cancellation check
                    if now - last_cancel_check >= CANCEL_CHECK_INTERVAL:
                        current = jobs.load_job(job_id)
                        if current and current.status == "cancelled":
                            log.info("⏹  [%s] cancelled by user", job_id)
                            proc.terminate()
                            cancelled = True
                            result_status = "cancelled"
                            break
                        last_cancel_check = now

                except (ValueError, IndexError):
                    pass

            # Timeout watchdog check (only if we've been processing a while)
            if now - last_output_time > cfg.FFMPEG_TIMEOUT:
                log.warning("⏱  [%s] ffmpeg timeout (no output for %ds)", job_id, cfg.FFMPEG_TIMEOUT)
                proc.kill()
                timed_out = True
                result_status = "timeout"
                break

    finally:
        # Unregister process
        unregister_process(job_id)

        stderr_output = proc.stderr.read() if proc.stderr else ""
        rc = proc.wait()
        elapsed = time.time() - last_output_time

        log.debug("[FFMPEG] [%s] process exited (rc=%d, elapsed_since_output=%.1fs)",
                  job_id, rc, elapsed)

        # Clear memory cache
        jobs.clear_progress_memory(job_id)

        if cancelled:
            log.debug("[FFMPEG] [%s] result: cancelled", job_id)
            pass
        elif timed_out:
            jobs.update_job(job_id, status="error:timeout")
            log.debug("[FFMPEG] [%s] result: timeout", job_id)
            result_status = "timeout"
        elif rc == 0:
            jobs.update_job(job_id, status="done", transcoded=last_time_sec)
            log.info("✓  [%s] finished (%.1fs)", job_id, last_time_sec)
            log.debug("[FFMPEG] [%s] result: done", job_id)
            result_status = "done"
        else:
            jobs.update_job(job_id, status=f"error:{rc}")
            log.error("✖︎  [%s] ffmpeg exit %s – stderr:\n%s", job_id, rc, stderr_output)
            log.debug("[FFMPEG] [%s] result: error:%d", job_id, rc)
            result_status = f"error:{rc}"

        # Log output directory stats
        try:
            segment_count = len(list(out_dir.glob("*.ts")))
            playlist_exists = (out_dir / "playlist.m3u8").exists()
            log.debug("[FFMPEG] [%s] output: %d segments, playlist=%s",
                      job_id, segment_count, playlist_exists)
        except Exception as e:
            log.debug("[FFMPEG] [%s] failed to stat output dir: %s", job_id, e)

    return result_status


def _process_job(job: Job) -> None:
    """
    Process a claimed job with automatic retry on failure.

    If the job fails and retry_count < MAX_JOB_RETRIES, re-queues the job
    for another attempt.
    """
    job_id = job.job_id
    src = Path(job.src).resolve()
    current_retry = int(job.retry_count)

    log.info("[JOB] processing job %s (retry=%d/%d)", job_id, current_retry, cfg.MAX_JOB_RETRIES)
    log.debug("[JOB] [%s] source: %s", job_id, src)

    try:
        params = jobs.TranscodeParams.model_validate_json(job.params_json)
        log.debug("[JOB] [%s] params parsed successfully", job_id)
    except Exception as e:
        log.error("[JOB] [%s] failed to parse params: %s", job_id, e, exc_info=True)
        jobs.update_job(job_id, status="error:params")
        return

    if not src.exists():
        log.error("[JOB] [%s] source file not found: %s", job_id, src)
        jobs.update_job(job_id, status="error:missing_source")
        return

    log.debug("[JOB] [%s] marking as working", job_id)
    jobs.update_job(job_id, status="working", started=time.time())

    result = _run_ffmpeg(job_id, src, params)
    log.debug("[JOB] [%s] ffmpeg result: %s", job_id, result)

    # On successful transcode, extract subtitles and generate thumbnails
    if result == "done":
        out_dir = cfg.HLS_DIR / job_id
        # Get job info for media_info and duration
        job_info = jobs.load_job(job_id)

        # Extract subtitles if available
        if job_info and job_info.media_info and job_info.media_info.subtitles:
            subtitles = [
                {
                    "index": s.index,
                    "codec": s.codec,
                    "language": s.language,
                    "title": s.title,
                }
                for s in job_info.media_info.subtitles
            ]
            extracted = _extract_subtitles(job_id, src, out_dir, subtitles)
            if extracted:
                jobs.update_extracted_subtitles(job_id, extracted)

        # Generate thumbnails for video content
        if job_info and params.media_type == "video":
            thumbnail_info = _generate_thumbnails(job_id, src, out_dir, job_info.duration)
            if thumbnail_info:
                jobs.update_thumbnails(job_id, thumbnail_info)

    # Handle retry logic for failures (not cancellations or success)
    if result not in ("done", "cancelled"):
        if current_retry < cfg.MAX_JOB_RETRIES:
            new_retry = current_retry + 1
            log.warning(
                "🔄  [%s] scheduling retry %d/%d",
                job_id, new_retry, cfg.MAX_JOB_RETRIES
            )
            jobs.update_job(
                job_id,
                status="queued",
                retry_count=new_retry,
                transcoded=0.0,
            )
        else:
            log.error(
                "❌  [%s] max retries (%d) exceeded, marking as failed",
                job_id, cfg.MAX_JOB_RETRIES
            )
    else:
        log.debug("[JOB] [%s] completed with status: %s", job_id, result)


def main() -> None:
    log.info("=" * 60)
    log.info("Worker starting")
    log.info("=" * 60)
    log.debug("[WORKER] HLS_DIR: %s", cfg.HLS_DIR)
    log.debug("[WORKER] WORKER_CONCURRENCY: %d", cfg.WORKER_CONCURRENCY)
    log.debug("[WORKER] FFMPEG_TIMEOUT: %d seconds", cfg.FFMPEG_TIMEOUT)
    log.debug("[WORKER] MAX_JOB_RETRIES: %d", cfg.MAX_JOB_RETRIES)

    # Validate ffmpeg installation before starting
    if not _validate_ffmpeg():
        log.error("FFmpeg validation failed – worker cannot start")
        log.error("Please ensure ffmpeg and ffprobe are installed and in PATH")
        return

    log.info("[WORKER] FFmpeg validation passed")

    # Detect hardware acceleration
    log.debug("[WORKER] detecting hardware acceleration...")
    hw_encoder, hw_type = _detect_hw_accel()
    if hw_encoder:
        log.info("[WORKER] Hardware acceleration: %s (%s)", hw_encoder, hw_type)
    else:
        log.info("[WORKER] Hardware acceleration: none (using software encoding)")

    # Set up signal handlers for graceful shutdown (only works in main thread)
    is_main = threading.current_thread() is threading.main_thread()
    log.debug("[WORKER] running in main thread: %s", is_main)
    if is_main:
        signal.signal(signal.SIGTERM, _handle_shutdown)
        signal.signal(signal.SIGINT, _handle_shutdown)
        log.debug("[WORKER] signal handlers registered")

    # Recover any stale jobs from previous crashes
    log.debug("[WORKER] checking for stale jobs...")
    recovered = recover_stale_jobs()
    if recovered:
        log.warning("[WORKER] recovered %d stale jobs from previous run", recovered)
    else:
        log.debug("[WORKER] no stale jobs found")

    log.info("[WORKER] ready – polling database, concurrency %d", cfg.WORKER_CONCURRENCY)
    executor = ThreadPoolExecutor(max_workers=cfg.WORKER_CONCURRENCY)
    futures = []
    last_cleanup = time.time()
    poll_count = 0

    while not _shutdown_requested:
        poll_count += 1

        # Periodic cleanup of old completed jobs
        if time.time() - last_cleanup > CLEANUP_INTERVAL:
            log.debug("[WORKER] running periodic cleanup...")
            try:
                jobs_del, dirs_del = cleanup_old_jobs()
                if jobs_del:
                    log.info("[CLEANUP] removed %d jobs, %d directories", jobs_del, dirs_del)
                else:
                    log.debug("[CLEANUP] nothing to clean up")
            except Exception:
                log.exception("[CLEANUP] cleanup failed")
            last_cleanup = time.time()

        # Try to claim a job
        job = claim_next_queued_job()
        if job is None:
            if poll_count % 100 == 0:  # Log every 50 seconds of idle
                log.debug("[WORKER] idle, waiting for jobs... (active=%d)", len(futures))
            time.sleep(POLL_INTERVAL)
            continue

        log.debug("[WORKER] claimed job %s, submitting to executor", job.job_id)
        future = executor.submit(_process_job, job)
        futures.append(future)

        # Clean up completed futures
        old_count = len(futures)
        futures = [f for f in futures if not f.done()]
        if old_count != len(futures):
            log.debug("[WORKER] cleaned up %d completed futures, %d active",
                      old_count - len(futures), len(futures))

    # Graceful shutdown: wait for in-progress jobs
    log.info("[WORKER] shutdown requested, cleaning up...")
    if futures:
        log.info("[WORKER] waiting for %d jobs to complete...", len(futures))
        wait(futures, timeout=600)

    log.debug("[WORKER] shutting down executor...")
    executor.shutdown(wait=True)
    log.info("[WORKER] shutdown complete")


if __name__ == "__main__":
    cfg.HLS_DIR.mkdir(parents=True, exist_ok=True)
    main()

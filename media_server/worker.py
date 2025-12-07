#!/usr/bin/env python3
"""
worker.py – background worker that polls the SQLite database for queued
transcode/remux jobs and runs ffmpeg to produce HLS output.

Features:
- Two-tier progress updates (memory: 1/sec, database: 1/30sec)
- Graceful shutdown on SIGTERM/SIGINT
- Periodic cleanup of old jobs
- Job cancellation support
- Zombie job recovery on startup
"""
from __future__ import annotations

import json
import logging
import signal
import shutil
import subprocess
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


def _handle_shutdown(signum, frame):
    global _shutdown_requested
    log.info("shutdown requested (signal %d), finishing current jobs...", signum)
    _shutdown_requested = True


def _run_ffmpeg(job_id: str, src: Path, p: jobs.TranscodeParams) -> None:
    """
    Execute one ffmpeg process with two-tier progress updates.

    - In-memory updates: every 1 second (for responsive UI)
    - Database persistence: every 30 seconds (reduces I/O)
    - Cancellation checks: every 2 seconds
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
            vf = (
                f"scale={p.width}:{p.height}:force_original_aspect_ratio=decrease,"
                f"pad={p.width}:{p.height}:(ow-iw)/2:(oh-ih)/2"
            )
            gop = segment_duration * 25
            bufsize = f"{2 * int(p.vb.rstrip('k'))}k"
            cmd += [
                "-vf",
                vf,
                "-c:v",
                p.video_codec,
                "-b:v",
                p.vb,
                "-maxrate",
                p.vb,
                "-bufsize",
                bufsize,
                "-g",
                str(gop),
                "-keyint_min",
                str(gop),
                "-sc_threshold",
                "0",
                "-preset",
                p.preset,
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
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    last_time_sec = 0.0
    last_memory_update = 0.0
    last_db_update = 0.0
    last_cancel_check = 0.0
    cancelled = False

    try:
        if proc.stdout is None:
            raise RuntimeError("ffmpeg stdout pipe missing")

        for ln in proc.stdout:
            if "out_time_ms=" in ln:
                try:
                    ms = int(ln.strip().split("=", 1)[1])
                    last_time_sec = ms / 1_000_000
                    now = time.time()

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
                            break
                        last_cancel_check = now

                except (ValueError, IndexError):
                    pass
    finally:
        stderr_output = proc.stderr.read() if proc.stderr else ""
        rc = proc.wait()

        # Clear memory cache
        jobs.clear_progress_memory(job_id)

        if cancelled:
            # Already logged, status already set
            pass
        elif rc == 0:
            jobs.update_job(job_id, status="done", transcoded=last_time_sec)
            log.info("✓  [%s] finished (%.1fs)", job_id, last_time_sec)
        else:
            jobs.update_job(job_id, status=f"error:{rc}")
            log.error("✖︎  [%s] ffmpeg exit %s – stderr:\n%s", job_id, rc, stderr_output)


def _process_job(job: Job) -> None:
    """Process a claimed job."""
    job_id = job.job_id
    src = Path(job.src).resolve()
    params = jobs.TranscodeParams.model_validate_json(job.params_json)

    jobs.update_job(job_id, status="working", started=time.time())
    _run_ffmpeg(job_id, src, params)


def main() -> None:
    # Set up signal handlers for graceful shutdown (only works in main thread)
    import threading
    if threading.current_thread() is threading.main_thread():
        signal.signal(signal.SIGTERM, _handle_shutdown)
        signal.signal(signal.SIGINT, _handle_shutdown)

    # Recover any stale jobs from previous crashes
    recovered = recover_stale_jobs()
    if recovered:
        log.warning("recovered %d stale jobs from previous run", recovered)

    log.info("worker ready – polling database, concurrency %i", cfg.WORKER_CONCURRENCY)
    executor = ThreadPoolExecutor(max_workers=cfg.WORKER_CONCURRENCY)
    futures = []
    last_cleanup = time.time()

    while not _shutdown_requested:
        # Periodic cleanup of old completed jobs
        if time.time() - last_cleanup > CLEANUP_INTERVAL:
            try:
                jobs_del, dirs_del = cleanup_old_jobs()
                if jobs_del:
                    log.info("cleanup: removed %d jobs, %d directories", jobs_del, dirs_del)
            except Exception:
                log.exception("cleanup failed")
            last_cleanup = time.time()

        # Try to claim a job
        job = claim_next_queued_job()
        if job is None:
            time.sleep(POLL_INTERVAL)
            continue

        future = executor.submit(_process_job, job)
        futures.append(future)

        # Clean up completed futures
        futures = [f for f in futures if not f.done()]

    # Graceful shutdown: wait for in-progress jobs
    if futures:
        log.info("waiting for %d jobs to complete...", len(futures))
        wait(futures, timeout=600)

    executor.shutdown(wait=True)
    log.info("worker shutdown complete")


if __name__ == "__main__":
    cfg.HLS_DIR.mkdir(parents=True, exist_ok=True)
    main()

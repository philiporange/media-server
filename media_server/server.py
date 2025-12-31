#!/usr/bin/env python3
"""
server.py – FastAPI front-end for the minimal HLS stack.

Features:
- Path traversal protection
- Health check endpoint
- Job cancellation
- Rate limiting
- Structured logging option
"""
from __future__ import annotations

import json as _json
import logging
import os
import threading
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

import mimetypes

import uvicorn
from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from media_server.config import cfg
from media_server import jobs
from media_server.jobs import JobInfo, TranscodeParams
from media_server.models import get_queue_stats

# optional worker autostart
from media_server import worker as _worker_module  # noqa: E402

# Resolve paths relative to this module
_HERE = Path(__file__).parent.resolve()
_STATIC_DIR = _HERE / "static"


# ─────────────────────────────────────────────────────────── logging setup

class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""

    def format(self, record):
        return _json.dumps({
            "ts": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        })


LOG_LVL = os.getenv("LOG_LEVEL", "INFO").upper()

if cfg.LOG_FORMAT == "json":
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logging.root.handlers = [handler]
    logging.root.setLevel(LOG_LVL)
else:
    logging.basicConfig(level=LOG_LVL, format="%(asctime)s %(levelname)-8s %(message)s")

log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────── worker daemon

def _start_worker_daemon() -> None:
    if getattr(_start_worker_daemon, "_started", False):
        return
    th = threading.Thread(target=_worker_module.main, name="db-worker", daemon=True)
    th.start()
    log.info("background worker thread started (id=%s)", th.ident)
    _start_worker_daemon._started = True  # type: ignore[attr-defined]


# ─────────────────────────────────────────────────────────── rate limiting

_request_times: dict[str, list[float]] = defaultdict(list)
_rate_limit_lock = threading.Lock()


def _check_rate_limit(client_ip: str) -> None:
    """Check and enforce rate limiting for a client IP."""
    now = time.time()
    window_start = now - cfg.RATE_LIMIT_WINDOW

    with _rate_limit_lock:
        # Clean old entries
        old_count = len(_request_times[client_ip])
        _request_times[client_ip] = [
            t for t in _request_times[client_ip] if t > window_start
        ]
        current_count = len(_request_times[client_ip])

        if old_count != current_count:
            log.debug("[RATE_LIMIT] %s: cleaned %d old entries", client_ip, old_count - current_count)

        if current_count >= cfg.RATE_LIMIT_REQUESTS:
            log.warning("[RATE_LIMIT] %s: limit exceeded (%d/%d)", client_ip, current_count, cfg.RATE_LIMIT_REQUESTS)
            raise HTTPException(429, "rate limit exceeded")

        _request_times[client_ip].append(now)
        log.debug("[RATE_LIMIT] %s: %d/%d requests in window", client_ip, current_count + 1, cfg.RATE_LIMIT_REQUESTS)


# ─────────────────────────────────────────────────────────── path security

MEDIA_DIR: Path = cfg.MEDIA_DIR
HLS_DIR: Path = cfg.HLS_DIR
MEDIA_EXTS = {
    # Video formats
    ".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v",
    # Audio formats
    ".mp3", ".flac", ".wav", ".m4a", ".aac", ".ogg", ".opus", ".wma"
}


def _safe_media_path(filename: str) -> Path:
    """
    Resolve filename within MEDIA_DIR, raising 404 if path escapes.

    Protects against path traversal attacks. If ALLOW_ABSOLUTE_PATHS is set,
    absolute paths are permitted (for trusted internal use).
    """
    log.debug("[PATH] resolving filename: %r", filename)

    # Check for absolute path mode
    if cfg.ALLOW_ABSOLUTE_PATHS and filename.startswith("/"):
        path = Path(filename)
        if ".." in filename:
            log.warning("[PATH] rejected absolute path with traversal: %r", filename)
            raise HTTPException(400, "invalid filename")
        log.debug("[PATH] absolute path allowed: %s", path)
        return path

    # Reject obvious traversal attempts early
    if ".." in filename or filename.startswith("/"):
        log.warning("[PATH] rejected path traversal attempt: %r", filename)
        raise HTTPException(400, "invalid filename")

    path = (MEDIA_DIR / filename).resolve()
    log.debug("[PATH] resolved to: %s", path)

    # Ensure resolved path is still within MEDIA_DIR
    try:
        path.relative_to(MEDIA_DIR)
    except ValueError:
        log.warning("[PATH] path escape detected: %s not in %s", path, MEDIA_DIR)
        raise HTTPException(404, "file not found")

    log.debug("[PATH] path validated: %s", path)
    return path


# ─────────────────────────────────────────────────────────── app setup

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
HLS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Media Server API")
_start_worker_daemon()

# CORS middleware for cross-origin HLS playback
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=_STATIC_DIR, html=True, check_dir=True), name="static_assets")
app.mount("/media", StaticFiles(directory=HLS_DIR, html=False, check_dir=True), name="media")

# MIME types
mimetypes.init()
mimetypes.add_type("application/vnd.apple.mpegurl", ".m3u8")
mimetypes.add_type("video/mp2t", ".ts")


# ─────────────────────────────────────────────────────────── routes

@app.get("/")
def index():
    log.debug("[ROUTE] GET / - serving index.html")
    idx = _STATIC_DIR / "index.html"
    if idx.is_file():
        return FileResponse(idx)
    log.error("[ROUTE] index.html not found at %s", idx)
    return PlainTextResponse("index.html not found", 404)


@app.get("/demo")
def demo():
    log.debug("[ROUTE] GET /demo - serving demo.html")
    idx = _STATIC_DIR / "demo.html"
    if idx.is_file():
        return FileResponse(idx)
    log.error("[ROUTE] demo.html not found at %s", idx)
    return PlainTextResponse("demo.html not found", 404)


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    log.debug("[ROUTE] GET /health - checking system health")
    try:
        stats = get_queue_stats()
        log.debug("[HEALTH] queue stats: %s", stats)
    except Exception as e:
        log.error("[HEALTH] database error: %s", e, exc_info=True)
        raise HTTPException(503, f"database error: {e}")

    return {
        "status": "healthy",
        "queue": stats,
        "media_dir": str(MEDIA_DIR),
        "hls_dir": str(HLS_DIR),
    }


@app.get("/list")
def list_media():
    log.debug("[ROUTE] GET /list - scanning %s", MEDIA_DIR)
    files = []
    try:
        for p in MEDIA_DIR.iterdir():
            if p.suffix.lower() in MEDIA_EXTS:
                try:
                    stat = p.stat()
                    files.append({
                        "name": p.name,
                        "ext": p.suffix.lower(),
                        "size": stat.st_size,
                        "is_audio": p.suffix.lower() in cfg.AUDIO_EXTENSIONS
                    })
                except OSError as e:
                    log.warning("[LIST] failed to stat %s: %s", p, e)
    except OSError as e:
        log.error("[LIST] failed to read directory %s: %s", MEDIA_DIR, e)
        raise HTTPException(500, f"failed to read media directory: {e}")

    result = sorted(files, key=lambda x: x["name"])
    log.debug("[LIST] found %d media files", len(result))
    return {"files": result}


@app.post("/stream/{filename:path}")
def start_stream(
    filename: str,
    request: Request,
    params: Optional[TranscodeParams] = Body(default=None),
):
    client_ip = request.client.host if request.client else "unknown"
    log.info("[STREAM] POST /stream/%s from %s", filename, client_ip)
    log.debug("[STREAM] params: %s", params.model_dump() if params else "auto")

    # Rate limiting
    _check_rate_limit(client_ip)

    # Path traversal protection
    src_path = _safe_media_path(filename)
    if not src_path.is_file():
        log.warning("[STREAM] file not found: %s", src_path)
        raise HTTPException(404, "media file not found")
    if src_path.suffix.lower() not in MEDIA_EXTS:
        log.warning("[STREAM] unsupported extension: %s", src_path.suffix)
        raise HTTPException(404, "media file not found")

    log.debug("[STREAM] source file: %s (%.1f MB)", src_path, src_path.stat().st_size / 1024 / 1024)

    try:
        info: JobInfo = jobs.enqueue_job(src_path, params)
        log.info("[STREAM] job created: %s (status=%s, duration=%.1fs)",
                 info.job_id, info.status, info.duration)
        log.debug("[STREAM] job params: %s", info.params.model_dump())
    except FileNotFoundError:
        log.error("[STREAM] file disappeared: %s", src_path)
        raise HTTPException(404, "media file not found")
    except Exception as e:
        log.error("[STREAM] failed to enqueue job: %s", e, exc_info=True)
        raise HTTPException(500, f"failed to create stream: {e}")

    return {
        "job_id": info.job_id,
        "playlist": info.playlist_url,
        "duration": info.duration,
        "media_type": info.params.media_type,
        "filename": filename,
        "params": info.params.model_dump()
    }


@app.get("/info/{job_id}")
def job_info(job_id: str):
    log.debug("[INFO] GET /info/%s", job_id)
    info = jobs.get_job(job_id)
    if info is None:
        log.debug("[INFO] job not found: %s", job_id)
        raise HTTPException(404, "unknown job id")
    log.debug("[INFO] job %s: status=%s, transcoded=%.1f/%.1f",
              job_id, info.status, info.transcoded, info.duration)
    return info.model_dump()


@app.post("/cancel/{job_id}")
def cancel_job(job_id: str):
    """Cancel a queued or in-progress job."""
    log.info("[CANCEL] POST /cancel/%s", job_id)
    info = jobs.get_job(job_id)
    if info is None:
        log.warning("[CANCEL] job not found: %s", job_id)
        raise HTTPException(404, "unknown job id")

    log.debug("[CANCEL] job %s current status: %s", job_id, info.status)

    if info.status == "done":
        log.warning("[CANCEL] cannot cancel completed job: %s", job_id)
        raise HTTPException(400, "job already completed")

    if info.status.startswith("error") or info.status == "cancelled":
        log.debug("[CANCEL] job %s already stopped: %s", job_id, info.status)
        return {"status": "already_stopped", "job_id": job_id}

    jobs.update_job(job_id, status="cancelled")
    log.info("[CANCEL] job %s marked as cancelled", job_id)

    # Attempt direct process termination for faster response
    if _worker_module.terminate_process(job_id):
        log.info("[CANCEL] directly terminated ffmpeg process for job %s", job_id)
    else:
        log.debug("[CANCEL] no active process found for job %s", job_id)

    return {"status": "cancelled", "job_id": job_id}


@app.get("/download/{filename:path}")
def download_file(filename: str):
    log.debug("[DOWNLOAD] GET /download/%s", filename)
    path = _safe_media_path(filename)
    if path.is_file():
        log.info("[DOWNLOAD] serving file: %s (%.1f MB)", path, path.stat().st_size / 1024 / 1024)
        return FileResponse(path, filename=path.name)
    log.warning("[DOWNLOAD] file not found: %s", path)
    raise HTTPException(404, "file not found")


def main():
    """Entry point for the media server."""
    log.info("=" * 60)
    log.info("Media Server starting")
    log.info("=" * 60)
    log.info("[CONFIG] MEDIA_DIR: %s", MEDIA_DIR)
    log.info("[CONFIG] HLS_DIR: %s", HLS_DIR)
    log.info("[CONFIG] LOG_LEVEL: %s", LOG_LVL)
    log.info("[CONFIG] LOG_FORMAT: %s", cfg.LOG_FORMAT)
    log.info("[CONFIG] WORKER_CONCURRENCY: %d", cfg.WORKER_CONCURRENCY)
    log.info("[CONFIG] RATE_LIMIT: %d requests / %d seconds", cfg.RATE_LIMIT_REQUESTS, cfg.RATE_LIMIT_WINDOW)
    log.info("[CONFIG] FFMPEG_TIMEOUT: %d seconds", cfg.FFMPEG_TIMEOUT)
    log.info("[CONFIG] MAX_JOB_RETRIES: %d", cfg.MAX_JOB_RETRIES)
    log.info("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8007, reload=False)


if __name__ == "__main__":
    main()

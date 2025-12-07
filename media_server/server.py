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
        _request_times[client_ip] = [
            t for t in _request_times[client_ip] if t > window_start
        ]

        if len(_request_times[client_ip]) >= cfg.RATE_LIMIT_REQUESTS:
            raise HTTPException(429, "rate limit exceeded")

        _request_times[client_ip].append(now)


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

    Protects against path traversal attacks.
    """
    # Reject obvious traversal attempts early
    if ".." in filename or filename.startswith("/"):
        raise HTTPException(400, "invalid filename")

    path = (MEDIA_DIR / filename).resolve()

    # Ensure resolved path is still within MEDIA_DIR
    try:
        path.relative_to(MEDIA_DIR)
    except ValueError:
        raise HTTPException(404, "file not found")

    return path


# ─────────────────────────────────────────────────────────── app setup

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
HLS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Media Server API")
_start_worker_daemon()

app.mount("/assets", StaticFiles(directory=_STATIC_DIR, html=True, check_dir=True), name="static_assets")
app.mount("/media", StaticFiles(directory=HLS_DIR, html=False, check_dir=True), name="media")

# MIME types
mimetypes.init()
mimetypes.add_type("application/vnd.apple.mpegurl", ".m3u8")
mimetypes.add_type("video/mp2t", ".ts")


# ─────────────────────────────────────────────────────────── routes

@app.get("/")
def index():
    idx = _STATIC_DIR / "index.html"
    return FileResponse(idx) if idx.is_file() else PlainTextResponse("index.html not found", 404)


@app.get("/demo")
def demo():
    idx = _STATIC_DIR / "demo.html"
    return FileResponse(idx) if idx.is_file() else PlainTextResponse("demo.html not found", 404)


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    try:
        stats = get_queue_stats()
    except Exception as e:
        raise HTTPException(503, f"database error: {e}")

    return {
        "status": "healthy",
        "queue": stats,
        "media_dir": str(MEDIA_DIR),
        "hls_dir": str(HLS_DIR),
    }


@app.get("/list")
def list_media():
    files = []
    for p in MEDIA_DIR.iterdir():
        if p.suffix.lower() in MEDIA_EXTS:
            files.append({
                "name": p.name,
                "ext": p.suffix.lower(),
                "size": p.stat().st_size,
                "is_audio": p.suffix.lower() in cfg.AUDIO_EXTENSIONS
            })
    return {"files": sorted(files, key=lambda x: x["name"])}


@app.post("/stream/{filename:path}")
def start_stream(
    filename: str,
    request: Request,
    params: Optional[TranscodeParams] = Body(default=None),
):
    # Rate limiting
    client_ip = request.client.host if request.client else "unknown"
    _check_rate_limit(client_ip)

    # Path traversal protection
    src_path = _safe_media_path(filename)
    if not src_path.is_file() or src_path.suffix.lower() not in MEDIA_EXTS:
        raise HTTPException(404, "media file not found")

    try:
        info: JobInfo = jobs.enqueue_job(src_path, params)
    except FileNotFoundError:
        raise HTTPException(404, "media file not found")

    return {
        "job_id": info.job_id,
        "playlist": info.playlist_url,
        "duration": info.duration,
        "media_type": info.params.media_type,
        "filename": filename
    }


@app.get("/info/{job_id}")
def job_info(job_id: str):
    info = jobs.get_job(job_id)
    if info is None:
        raise HTTPException(404, "unknown job id")
    return info.model_dump()


@app.post("/cancel/{job_id}")
def cancel_job(job_id: str):
    """Cancel a queued or in-progress job."""
    info = jobs.get_job(job_id)
    if info is None:
        raise HTTPException(404, "unknown job id")

    if info.status == "done":
        raise HTTPException(400, "job already completed")

    if info.status.startswith("error") or info.status == "cancelled":
        return {"status": "already_stopped", "job_id": job_id}

    jobs.update_job(job_id, status="cancelled")
    return {"status": "cancelled", "job_id": job_id}


@app.get("/download/{filename:path}")
def download_file(filename: str):
    path = _safe_media_path(filename)
    if path.is_file():
        return FileResponse(path, filename=path.name)
    raise HTTPException(404, "file not found")


def main():
    """Entry point for the media server."""
    uvicorn.run(app, host="0.0.0.0", port=8007, reload=False)


if __name__ == "__main__":
    main()

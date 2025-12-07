"""
Centralised runtime configuration for the media-server stack.

All settings can be overridden with environment variables.
"""
from __future__ import annotations

import os
from pathlib import Path


class Config:
    # Worker concurrency
    WORKER_CONCURRENCY: int = int(os.getenv("WORKER_CONCURRENCY", "4"))

    # Paths
    MEDIA_DIR: Path = Path(os.getenv("MEDIA_DIR", "/tmp/media")).absolute()
    HLS_DIR: Path = Path(os.getenv("HLS_DIR", str(MEDIA_DIR / "hls_output"))).absolute()
    DATABASE_PATH: Path = Path(
        os.getenv("DATABASE_PATH", str(MEDIA_DIR / "media_server.db"))
    ).absolute()

    # Video-specific settings
    SEGMENT_DURATION: int = int(os.getenv("HLS_TIME", "6"))  # seconds
    BUFFER_AHEAD_SEGMENTS: int = int(os.getenv("BUFFER_LENGTH", "15"))

    # Audio-specific settings
    AUDIO_SEGMENT_DURATION: int = int(os.getenv("AUDIO_SEGMENT_DURATION", "10"))
    AUDIO_EXTENSIONS: set = {".mp3", ".flac", ".wav", ".m4a", ".aac", ".ogg", ".opus", ".wma"}

    # Job management
    JOB_RETENTION_HOURS: int = int(os.getenv("JOB_RETENTION_HOURS", "168"))  # 7 days
    STALE_JOB_TIMEOUT: int = int(os.getenv("STALE_JOB_TIMEOUT", "3600"))  # 1 hour

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds

    # Logging
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # "text" or "json"


# Convenience singleton
cfg = Config()

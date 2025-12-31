"""
Centralised runtime configuration for the media-server stack.

All settings can be overridden with environment variables:

- WORKER_CONCURRENCY: Number of parallel transcoding jobs (default: 4)
- MEDIA_DIR: Source media directory (default: /tmp/media)
- HLS_DIR: HLS output directory (default: MEDIA_DIR/hls_output)
- DATABASE_PATH: SQLite database path (default: MEDIA_DIR/media_server.db)
- HLS_TIME: Video segment duration in seconds (default: 6)
- AUDIO_SEGMENT_DURATION: Audio segment duration in seconds (default: 10)
- JOB_RETENTION_HOURS: Auto-cleanup completed jobs after N hours (default: 168)
- STALE_JOB_TIMEOUT: Recover stuck jobs after N seconds (default: 3600)
- MAX_JOB_RETRIES: Retry failed jobs N times before giving up (default: 1)
- FFMPEG_TIMEOUT: Kill ffmpeg if no output for N seconds (default: 120)
- RATE_LIMIT_REQUESTS: Max requests per window (default: 10)
- RATE_LIMIT_WINDOW: Rate limit window in seconds (default: 60)
- LOG_FORMAT: Logging format, "text" or "json" (default: text)
- ALLOW_ABSOLUTE_PATHS: Allow absolute paths in API (default: false)
- HW_ACCEL: Hardware acceleration mode: auto, vaapi, nvenc, qsv, none (default: auto)
- EXTRACT_SUBTITLES: Extract embedded subtitles to WebVTT (default: true)
- GENERATE_THUMBNAILS: Generate seek preview thumbnails (default: true)
- THUMBNAIL_INTERVAL: Seconds between thumbnail captures (default: 10)
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
    MAX_JOB_RETRIES: int = int(os.getenv("MAX_JOB_RETRIES", "1"))  # retry once on failure

    # FFmpeg settings
    FFMPEG_TIMEOUT: int = int(os.getenv("FFMPEG_TIMEOUT", "120"))  # seconds with no output before killing

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds

    # Logging
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # "text" or "json"

    # Security
    ALLOW_ABSOLUTE_PATHS: bool = os.getenv("ALLOW_ABSOLUTE_PATHS", "false").lower() == "true"

    # Hardware acceleration: auto, vaapi, nvenc, qsv, none
    HW_ACCEL: str = os.getenv("HW_ACCEL", "auto").lower()

    # Subtitle extraction
    EXTRACT_SUBTITLES: bool = os.getenv("EXTRACT_SUBTITLES", "true").lower() == "true"

    # Thumbnail generation
    GENERATE_THUMBNAILS: bool = os.getenv("GENERATE_THUMBNAILS", "true").lower() == "true"
    THUMBNAIL_INTERVAL: int = int(os.getenv("THUMBNAIL_INTERVAL", "10"))  # seconds between thumbnails
    THUMBNAIL_WIDTH: int = int(os.getenv("THUMBNAIL_WIDTH", "160"))  # thumbnail width in pixels


# Convenience singleton
cfg = Config()

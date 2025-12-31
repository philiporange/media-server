#!/usr/bin/env python3
"""
run_server.py – Entry point for the media server.

Usage:
    python run_server.py

Environment variables:
    MEDIA_DIR          – Directory containing media files (default: ./media)
    HLS_DIR            – Directory for HLS output segments (default: ./hls_output)
    LOG_LEVEL          – Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
    LOG_FORMAT         – Log format: text or json (default: text)
    WORKER_CONCURRENCY – Number of concurrent transcode workers (default: 2)
    RATE_LIMIT_REQUESTS – Max requests per window (default: 30)
    RATE_LIMIT_WINDOW  – Rate limit window in seconds (default: 60)
    FFMPEG_TIMEOUT     – Timeout for ffmpeg processes in seconds (default: 120)
    MAX_JOB_RETRIES    – Number of retry attempts for failed jobs (default: 1)
    ALLOW_ABSOLUTE_PATHS – Allow absolute file paths (default: false)
"""

from media_server.server import main

if __name__ == "__main__":
    main()

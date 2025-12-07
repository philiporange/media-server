# Media Server

A high-performance HLS (HTTP Live Streaming) media server built with FastAPI. Handles video and audio streaming with smart transcoding and remuxing.

## Features

- Universal video and audio format support
- Smart processing: remux for compatible formats (H.264+AAC), transcode otherwise
- HLS streaming with progressive output
- Built-in web player and embeddable widget
- SQLite job queue with Peewee ORM
- Background worker with graceful shutdown

## Requirements

- Python 3.8+
- FFmpeg (with libx264 and AAC support)

## Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Create media directory
mkdir -p /tmp/media

# Add media files
cp your-videos/* /tmp/media/

# Start the server (includes background worker)
python -m media_server.server
```

Server runs at http://localhost:8007

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| MEDIA_DIR | /tmp/media | Source media directory |
| HLS_DIR | $MEDIA_DIR/hls_output | HLS output directory |
| DATABASE_PATH | $MEDIA_DIR/media_server.db | SQLite database path |
| WORKER_CONCURRENCY | 4 | Parallel transcoding jobs |
| JOB_RETENTION_HOURS | 168 | Auto-cleanup after N hours |
| HLS_TIME | 6 | Video segment duration (seconds) |
| AUDIO_SEGMENT_DURATION | 10 | Audio segment duration (seconds) |
| LOG_FORMAT | text | Logging format (text or json) |
| LOG_LEVEL | INFO | Logging level |

## Supported Formats

**Video**: MP4, MKV, MOV, AVI, WebM, FLV, WMV, M4V

**Audio**: MP3, FLAC, WAV, AAC, M4A, OGG, Opus, WMA

## API

See [USAGE.md](USAGE.md) for complete API documentation.

Quick examples:

```bash
# Stream a file
curl -X POST http://localhost:8007/stream/movie.mp4

# Check job status
curl http://localhost:8007/info/{job_id}

# List available media
curl http://localhost:8007/list

# Health check
curl http://localhost:8007/health
```

## Web Interface

- Main player: http://localhost:8007/
- Direct file access: http://localhost:8007/index.html?file=movie.mp4
- Embed demo: http://localhost:8007/demo

## Project Structure

```
media_server/
├── config.py      # Configuration management
├── models.py      # Peewee ORM models
├── server.py      # FastAPI web server
├── worker.py      # Background transcoding worker
├── jobs.py        # Job management
└── static/        # Web interface assets
```

## Author

Philip Orange <git@philiporange.com>

## License

CC0

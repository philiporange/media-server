# Media Server API Usage

Complete reference for the Media Server REST API.

## Overview

The Media Server provides HLS streaming for video and audio files. When you request a stream, the server:

1. Analyzes the source file with FFprobe
2. Decides whether to remux (copy streams) or transcode
3. Queues a job for the background worker
4. Returns a job ID and playlist URL
5. The worker processes the file into HLS segments
6. Clients can start playback before processing completes

## Base URL

Default: `http://localhost:8007`

## Endpoints

### POST /stream/{filename}

Start streaming a media file. Creates a transcoding job and returns the HLS playlist URL.

**Path Parameters:**
- `filename` (required): Path to media file relative to MEDIA_DIR

**Request Body (optional):**
```json
{
  "media_type": "video",
  "video_codec": "libx264",
  "audio_codec": "aac",
  "width": 1280,
  "height": 720,
  "vb": "2500k",
  "ab": "128k",
  "preset": "fast"
}
```

**Parameters:**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| media_type | string | "video" | Either "video" or "audio" |
| video_codec | string | "copy" | Video codec (libx264, copy) |
| audio_codec | string | "copy" | Audio codec (aac, copy) |
| width | int | null | Output width (required if transcoding video) |
| height | int | null | Output height (required if transcoding video) |
| vb | string | "0k" | Video bitrate (e.g., "2500k") |
| ab | string | "128k" | Audio bitrate (e.g., "192k") |
| preset | string | "fast" | x264 preset (ultrafast, fast, medium, slow) |

**Auto-Detection:**
If no body is provided, or if both codecs are "copy", the server automatically detects the optimal settings:

- **H.264+AAC video**: Remux (copy both streams, near-instant)
- **Other video formats**: Transcode to H.264+AAC
- **AAC audio**: Remux (copy stream)
- **Other audio formats**: Transcode to AAC

**Example Requests:**

```bash
# Auto-detect optimal settings (recommended)
curl -X POST http://localhost:8007/stream/movie.mp4

# With empty body (same as above)
curl -X POST http://localhost:8007/stream/movie.mp4 \
  -H "Content-Type: application/json" \
  -d '{}'

# Force specific transcoding settings
curl -X POST http://localhost:8007/stream/video.mkv \
  -H "Content-Type: application/json" \
  -d '{
    "media_type": "video",
    "video_codec": "libx264",
    "audio_codec": "aac",
    "width": 1920,
    "height": 1080,
    "vb": "5000k",
    "ab": "192k",
    "preset": "medium"
  }'

# Stream audio file
curl -X POST http://localhost:8007/stream/podcast.mp3
```

**Response:**
```json
{
  "job_id": "abc123def456",
  "playlist": "/media/abc123def456/playlist.m3u8",
  "duration": 7842.5,
  "media_type": "video",
  "filename": "movie.mp4"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| job_id | string | Unique job identifier (12 characters) |
| playlist | string | Relative URL to HLS playlist |
| duration | float | Media duration in seconds |
| media_type | string | Either "video" or "audio" |
| filename | string | Original filename |

**Errors:**
- `400`: Invalid filename (path traversal attempt)
- `404`: File not found or unsupported format
- `429`: Rate limit exceeded

---

### GET /info/{job_id}

Get current status and progress of a transcoding job.

**Path Parameters:**
- `job_id` (required): Job identifier from /stream response

**Example:**
```bash
curl http://localhost:8007/info/abc123def456
```

**Response:**
```json
{
  "job_id": "abc123def456",
  "src": "/tmp/media/movie.mp4",
  "duration": 7842.5,
  "playlist_url": "/media/abc123def456/playlist.m3u8",
  "started": 1701849600.123,
  "status": "working",
  "transcoded": 1234.5,
  "params": {
    "media_type": "video",
    "video_codec": "copy",
    "audio_codec": "copy",
    "width": null,
    "height": null,
    "vb": "0k",
    "ab": "128k",
    "preset": "fast"
  }
}
```

**Status Values:**
| Status | Description |
|--------|-------------|
| queued | Waiting for worker to pick up |
| claimed | Worker has claimed the job |
| working | Currently processing |
| done | Processing complete |
| cancelled | Cancelled by user |
| error:N | Failed with exit code N |

**Progress Calculation:**
```
progress_percent = (transcoded / duration) * 100
```

**Errors:**
- `404`: Unknown job ID

---

### POST /cancel/{job_id}

Cancel a queued or in-progress job.

**Path Parameters:**
- `job_id` (required): Job identifier

**Example:**
```bash
curl -X POST http://localhost:8007/cancel/abc123def456
```

**Response (success):**
```json
{
  "status": "cancelled",
  "job_id": "abc123def456"
}
```

**Response (already stopped):**
```json
{
  "status": "already_stopped",
  "job_id": "abc123def456"
}
```

**Errors:**
- `400`: Job already completed
- `404`: Unknown job ID

---

### GET /list

List all media files available for streaming.

**Example:**
```bash
curl http://localhost:8007/list
```

**Response:**
```json
{
  "files": [
    {
      "name": "movie.mp4",
      "ext": ".mp4",
      "size": 1073741824,
      "is_audio": false
    },
    {
      "name": "podcast.mp3",
      "ext": ".mp3",
      "size": 52428800,
      "is_audio": true
    }
  ]
}
```

**File Object Fields:**
| Field | Type | Description |
|-------|------|-------------|
| name | string | Filename |
| ext | string | File extension (lowercase) |
| size | int | File size in bytes |
| is_audio | bool | True if audio-only file |

---

### GET /health

Health check endpoint for monitoring.

**Example:**
```bash
curl http://localhost:8007/health
```

**Response:**
```json
{
  "status": "healthy",
  "queue": {
    "queued": 2,
    "working": 1,
    "done": 45,
    "cancelled": 0,
    "errors": 1
  },
  "media_dir": "/tmp/media",
  "hls_dir": "/tmp/media/hls_output"
}
```

**Queue Stats:**
| Field | Description |
|-------|-------------|
| queued | Jobs waiting to be processed |
| working | Jobs currently being processed |
| done | Completed jobs |
| cancelled | Cancelled jobs |
| errors | Failed jobs |

**Errors:**
- `503`: Database error

---

### GET /download/{filename}

Download original media file.

**Path Parameters:**
- `filename` (required): Path to file relative to MEDIA_DIR

**Example:**
```bash
curl -O http://localhost:8007/download/movie.mp4
```

**Errors:**
- `400`: Invalid filename
- `404`: File not found

---

### GET /

Serve the web player interface.

---

### GET /demo

Serve the embed demo page.

---

## Static Mounts

### /assets/*

Static files (JavaScript, CSS) from the static directory.

### /media/*

HLS output files (playlists and segments).

**Example:**
```
/media/{job_id}/playlist.m3u8
/media/{job_id}/segment000.ts
/media/{job_id}/segment001.ts
```

---

## Playback

### HLS.js (Browser)

```javascript
const video = document.querySelector('video');
const hls = new Hls();
hls.loadSource('http://localhost:8007/media/abc123def456/playlist.m3u8');
hls.attachMedia(video);
```

### Video.js

```javascript
videojs('player', {
  sources: [{
    src: 'http://localhost:8007/media/abc123def456/playlist.m3u8',
    type: 'application/x-mpegURL'
  }]
});
```

### ffplay

```bash
ffplay http://localhost:8007/media/abc123def456/playlist.m3u8
```

### VLC

```bash
vlc http://localhost:8007/media/abc123def456/playlist.m3u8
```

---

## Embedding

### Script Tag

```html
<script src="http://localhost:8007/assets/embed.js"
        data-file="movie.mp4"
        data-width="640"
        data-height="360"></script>
```

### JavaScript API

```javascript
MediaEmbed.init({
  file: 'movie.mp4',
  target: document.getElementById('player'),
  width: 800,
  height: 450,
  autoplay: false
});
```

**Embed Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| file | string | required | Media filename |
| target | Element | script location | Container element |
| width | number | 640 | Player width in pixels |
| height | number | 360 | Player height in pixels |
| autoplay | boolean | true | Auto-start playback |
| muted | boolean | false | Start muted |
| fullPage | boolean | false | Full page mode |

---

## Rate Limiting

The /stream endpoint is rate-limited to prevent abuse.

**Defaults:**
- 10 requests per 60 seconds per IP

**Configuration:**
```bash
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
```

**Error Response:**
```json
{
  "detail": "rate limit exceeded"
}
```
HTTP Status: 429

---

## Job Lifecycle

1. **queued**: Job created, waiting for worker
2. **claimed**: Worker has picked up the job
3. **working**: FFmpeg is processing
4. **done**: Processing complete, HLS files ready
5. **cancelled**: User cancelled the job
6. **error:N**: FFmpeg exited with code N

Jobs are automatically cleaned up after JOB_RETENTION_HOURS (default: 168 hours / 7 days).

---

## Workflow Examples

### Simple Streaming

```bash
# 1. Start streaming
response=$(curl -s -X POST http://localhost:8007/stream/video.mp4)
job_id=$(echo $response | jq -r '.job_id')
playlist=$(echo $response | jq -r '.playlist')

# 2. Poll for completion (optional - can start playback immediately)
while true; do
  status=$(curl -s http://localhost:8007/info/$job_id | jq -r '.status')
  if [ "$status" = "done" ]; then
    echo "Ready!"
    break
  fi
  sleep 1
done

# 3. Play
ffplay "http://localhost:8007$playlist"
```

### Progress Monitoring

```bash
# Watch transcoding progress
job_id="abc123def456"
while true; do
  info=$(curl -s http://localhost:8007/info/$job_id)
  status=$(echo $info | jq -r '.status')
  transcoded=$(echo $info | jq -r '.transcoded')
  duration=$(echo $info | jq -r '.duration')

  if [ "$status" = "done" ]; then
    echo "Complete!"
    break
  elif [[ "$status" == error* ]]; then
    echo "Failed: $status"
    break
  fi

  percent=$(echo "scale=1; $transcoded / $duration * 100" | bc)
  echo "Progress: ${percent}% ($status)"
  sleep 2
done
```

### Batch Processing

```bash
# Queue multiple files
for file in $(curl -s http://localhost:8007/list | jq -r '.files[].name'); do
  echo "Queueing: $file"
  curl -s -X POST "http://localhost:8007/stream/$file" | jq -r '.job_id'
done

# Monitor queue
curl -s http://localhost:8007/health | jq '.queue'
```

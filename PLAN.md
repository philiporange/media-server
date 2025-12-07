# Media Server Improvement Plan

Prioritized list of improvements ordered by impact and risk.

## 1. Zombie Job Recovery (High Priority)

**Problem**: If a worker crashes or the server restarts while a job is in "working" or "claimed" status, that job is stuck forever. Users would need to manually modify the database or wait for the file to change (triggering a new job ID).

**Solution**: On worker startup, reset stale jobs back to "queued" status.

```python
# models.py - add function
def recover_stale_jobs(max_age_seconds: float = 3600) -> int:
    """
    Reset jobs stuck in 'working' or 'claimed' status back to 'queued'.
    Returns number of recovered jobs.
    """
    import time
    cutoff = time.time() - max_age_seconds
    with db.atomic():
        count = (
            Job.update(status="queued")
            .where(
                (Job.status.in_(["working", "claimed"]))
                & (Job.started < cutoff)
            )
            .execute()
        )
    return count
```

```python
# worker.py - call on startup in main()
def main() -> None:
    recovered = recover_stale_jobs(max_age_seconds=3600)
    if recovered:
        log.warning("recovered %d stale jobs", recovered)
    log.info("worker ready – polling database, concurrency %i", cfg.WORKER_CONCURRENCY)
    # ... rest of main
```

---

## 2. Progress Update Throttling (High Priority)

**Problem**: FFmpeg emits progress updates many times per second. Each update triggers a database write, causing unnecessary I/O and potential SQLite lock contention.

**Solution**: Two-tier progress tracking:
- **In-memory cache**: Updated at most once per second, used by API for responsive UI
- **Database persistence**: Updated every 30 seconds, survives restarts

```python
# jobs.py - add in-memory progress cache
import threading

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
```

```python
# jobs.py - modify get_job to use cache
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
```

```python
# worker.py - modify _run_ffmpeg
def _run_ffmpeg(job_id: str, src: Path, p: jobs.TranscodeParams) -> None:
    # ... existing setup code ...

    last_time_sec = 0.0
    last_memory_update = 0.0
    last_db_update = 0.0
    MEMORY_INTERVAL = 1.0    # in-memory update: once per second
    DB_INTERVAL = 30.0       # database persist: every 30 seconds

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
                    if now - last_memory_update >= MEMORY_INTERVAL:
                        jobs.update_progress_memory(job_id, last_time_sec)
                        last_memory_update = now

                    # Low-frequency database persistence
                    if now - last_db_update >= DB_INTERVAL:
                        jobs.update_job(job_id, transcoded=last_time_sec)
                        last_db_update = now

                except (ValueError, IndexError):
                    pass
    finally:
        stderr_output = proc.stderr.read() if proc.stderr else ""
        rc = proc.wait()

        # Clear memory cache and persist final state
        jobs.clear_progress_memory(job_id)

        if rc == 0:
            jobs.update_job(job_id, status="done", transcoded=last_time_sec)
            log.info("✓  [%s] finished (%.1fs)", job_id, last_time_sec)
        else:
            jobs.update_job(job_id, status=f"error:{rc}")
            log.error("✖︎  [%s] ffmpeg exit %s – stderr:\n%s", job_id, rc, stderr_output)
```

This reduces database writes from hundreds per second to ~2 per minute, while still providing second-level progress granularity to the UI.

---

## 3. Job and HLS Cleanup (High Priority)

**Problem**: Completed jobs and their HLS output directories accumulate indefinitely, eventually filling the disk.

**Solution**: Add cleanup functions and a configurable retention period.

```python
# config.py - add setting
JOB_RETENTION_HOURS: int = int(os.getenv("JOB_RETENTION_HOURS", "168"))  # 7 days
```

```python
# models.py - add cleanup function
def cleanup_old_jobs(retention_hours: int = 168) -> tuple[int, int]:
    """
    Delete jobs older than retention_hours and their HLS directories.
    Returns (jobs_deleted, dirs_deleted).
    """
    import shutil
    import time
    from config import cfg

    cutoff = time.time() - (retention_hours * 3600)

    old_jobs = list(
        Job.select(Job.job_id)
        .where((Job.status == "done") & (Job.started < cutoff))
    )

    dirs_deleted = 0
    for job in old_jobs:
        hls_dir = cfg.HLS_DIR / job.job_id
        if hls_dir.exists():
            shutil.rmtree(hls_dir, ignore_errors=True)
            dirs_deleted += 1

    jobs_deleted = (
        Job.delete()
        .where((Job.status == "done") & (Job.started < cutoff))
        .execute()
    )

    return jobs_deleted, dirs_deleted
```

```python
# worker.py - periodic cleanup in main loop
CLEANUP_INTERVAL = 3600  # hourly

def main() -> None:
    # ... existing startup ...
    last_cleanup = time.time()

    while True:
        # Periodic cleanup
        if time.time() - last_cleanup > CLEANUP_INTERVAL:
            try:
                jobs_del, dirs_del = cleanup_old_jobs(cfg.JOB_RETENTION_HOURS)
                if jobs_del:
                    log.info("cleanup: removed %d jobs, %d directories", jobs_del, dirs_del)
            except Exception:
                log.exception("cleanup failed")
            last_cleanup = time.time()

        # ... existing job polling ...
```

---

## 4. Path Traversal Protection (High Priority)

**Problem**: While `resolve()` is used, there's no explicit check that the resolved path is still within MEDIA_DIR. A filename like `../../../etc/passwd` could potentially escape.

**Solution**: Add explicit containment check.

```python
# server.py - add helper function
def _safe_media_path(filename: str) -> Path:
    """
    Resolve filename within MEDIA_DIR, raising 404 if path escapes.
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
```

```python
# server.py - update endpoints
@app.post("/stream/{filename:path}")
def start_stream(filename: str, params: Optional[TranscodeParams] = Body(default=None)):
    src_path = _safe_media_path(filename)
    if not src_path.is_file() or src_path.suffix.lower() not in MEDIA_EXTS:
        raise HTTPException(404, "media file not found")
    # ... rest unchanged ...

@app.get("/download/{filename:path}")
def download_file(filename: str):
    path = _safe_media_path(filename)
    if path.is_file():
        return FileResponse(path, filename=path.name)
    raise HTTPException(404, "file not found")
```

---

## 5. Database Connection Handling (Medium Priority)

**Problem**: Peewee's default connection handling isn't ideal for multi-threaded workers. Each thread should manage its own connection.

**Solution**: Use explicit connection management per-thread.

```python
# models.py - update database setup
from playhouse.pool import PooledSqliteDatabase

db = PooledSqliteDatabase(
    str(cfg.DATABASE_PATH),
    max_connections=cfg.WORKER_CONCURRENCY + 2,
    stale_timeout=300,
    pragmas={
        "journal_mode": "wal",
        "cache_size": -64 * 1024,
        "synchronous": "normal",
    },
)
```

```python
# jobs.py - use connection context for updates
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
```

---

## 6. Graceful Worker Shutdown (Medium Priority)

**Problem**: When the worker process receives SIGTERM/SIGINT, it exits immediately, potentially leaving jobs in an inconsistent state.

**Solution**: Handle signals and wait for in-progress jobs.

```python
# worker.py - add signal handling
import signal
from concurrent.futures import ThreadPoolExecutor, wait

_shutdown_requested = False

def _handle_shutdown(signum, frame):
    global _shutdown_requested
    log.info("shutdown requested, finishing current jobs...")
    _shutdown_requested = True

def main() -> None:
    signal.signal(signal.SIGTERM, _handle_shutdown)
    signal.signal(signal.SIGINT, _handle_shutdown)

    log.info("worker ready – polling database, concurrency %i", cfg.WORKER_CONCURRENCY)
    executor = ThreadPoolExecutor(max_workers=cfg.WORKER_CONCURRENCY)
    futures = []

    while not _shutdown_requested:
        job = claim_next_queued_job()
        if job is None:
            time.sleep(POLL_INTERVAL)
            continue

        future = executor.submit(_process_job, job)
        futures.append(future)

        # Clean up completed futures
        futures = [f for f in futures if not f.done()]

    # Wait for in-progress jobs to complete
    if futures:
        log.info("waiting for %d jobs to complete...", len(futures))
        wait(futures, timeout=600)

    executor.shutdown(wait=True)
    log.info("worker shutdown complete")
```

---

## 7. Health Check Endpoint (Medium Priority)

**Problem**: No way to monitor if the server and worker are healthy in production.

**Solution**: Add health endpoint with queue status.

```python
# server.py - add health endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    from models import Job, db

    try:
        with db.connection_context():
            queued = Job.select().where(Job.status == "queued").count()
            working = Job.select().where(Job.status.in_(["working", "claimed"])).count()
            done = Job.select().where(Job.status == "done").count()
            errors = Job.select().where(Job.status.startswith("error")).count()
    except Exception as e:
        raise HTTPException(503, f"database error: {e}")

    return {
        "status": "healthy",
        "queue": {
            "queued": queued,
            "working": working,
            "done": done,
            "errors": errors,
        },
        "media_dir": str(MEDIA_DIR),
        "hls_dir": str(HLS_DIR),
    }
```

---

## 8. Job Cancellation (Medium Priority)

**Problem**: No way to cancel a queued or in-progress job.

**Solution**: Add cancel endpoint and check for cancellation in worker.

```python
# server.py - add cancel endpoint
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
```

```python
# worker.py - check for cancellation during processing
def _run_ffmpeg(job_id: str, src: Path, p: jobs.TranscodeParams) -> None:
    # ... setup ...

    for ln in proc.stdout:
        # Check if job was cancelled
        current = jobs.get_job(job_id)
        if current and current.status == "cancelled":
            proc.terminate()
            log.info("⏹  [%s] cancelled by user", job_id)
            return

        # ... existing progress handling ...
```

---

## 9. Request Rate Limiting (Lower Priority)

**Problem**: The `/stream` endpoint triggers CPU-intensive transcoding. Without rate limiting, abuse could exhaust server resources.

**Solution**: Add simple in-memory rate limiting.

```python
# server.py - add rate limiter
from collections import defaultdict
import time

_request_times: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60  # seconds

def _check_rate_limit(client_ip: str) -> None:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    # Clean old entries
    _request_times[client_ip] = [
        t for t in _request_times[client_ip] if t > window_start
    ]

    if len(_request_times[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(429, "rate limit exceeded")

    _request_times[client_ip].append(now)

@app.post("/stream/{filename:path}")
def start_stream(
    filename: str,
    request: Request,
    params: Optional[TranscodeParams] = Body(default=None),
):
    _check_rate_limit(request.client.host if request.client else "unknown")
    # ... rest of endpoint ...
```

---

## 10. Structured Logging (Lower Priority)

**Problem**: Current logging is plain text, making it harder to parse in log aggregation systems.

**Solution**: Add JSON logging option for production.

```python
# config.py - add setting
LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # "text" or "json"
```

```python
# server.py / worker.py - conditional formatting
import json as _json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return _json.dumps({
            "ts": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        })

if cfg.LOG_FORMAT == "json":
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logging.root.handlers = [handler]
```

---

## Implementation Order

1. **Path Traversal Protection** - Security fix, implement immediately
2. **Zombie Job Recovery** - Data integrity, high impact
3. **Progress Update Throttling** - Performance, easy win
4. **Job Cleanup** - Prevents disk exhaustion
5. **Health Check Endpoint** - Enables monitoring
6. **Graceful Shutdown** - Production reliability
7. **Database Connection Handling** - Stability under load
8. **Job Cancellation** - User experience
9. **Rate Limiting** - Abuse prevention
10. **Structured Logging** - Operational improvement

"""
models.py – Peewee ORM models for storing transcoding job metadata in SQLite.

The Job model stores all job state including transcode parameters as JSON.
Queue functionality is implemented via status field polling.
"""
from __future__ import annotations

import shutil
import time
import threading
from pathlib import Path

from peewee import (
    Model,
    CharField,
    FloatField,
    TextField,
    SqliteDatabase,
)

from media_server.config import cfg

# Ensure database directory exists
cfg.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# Thread-safe database connection
# Using SqliteDatabase with check_same_thread=False for multi-threaded access
db = SqliteDatabase(
    str(cfg.DATABASE_PATH),
    pragmas={
        "journal_mode": "wal",
        "cache_size": -64 * 1024,  # 64MB cache
        "synchronous": "normal",
        "foreign_keys": 1,
    },
    check_same_thread=False,
)

_db_lock = threading.Lock()


class BaseModel(Model):
    class Meta:
        database = db


class Job(BaseModel):
    """Transcoding job record."""

    job_id = CharField(primary_key=True, max_length=12)
    src = TextField()
    duration = FloatField()
    playlist_url = TextField()
    started = FloatField()
    status = CharField(max_length=32, index=True)
    transcoded = FloatField(default=0.0)
    params_json = TextField()  # JSON-serialized TranscodeParams

    class Meta:
        table_name = "jobs"


def init_db() -> None:
    """Create tables if they don't exist."""
    with db.connection_context():
        db.create_tables([Job], safe=True)


def claim_next_queued_job() -> Job | None:
    """
    Atomically claim the next queued job by updating its status to 'claimed'.

    Returns the Job if one was claimed, None if queue is empty.
    Uses a transaction to prevent race conditions between workers.
    """
    with _db_lock:
        with db.atomic():
            job = (
                Job.select()
                .where(Job.status == "queued")
                .order_by(Job.started)
                .first()
            )
            if job:
                job.status = "claimed"
                job.save()
                return job
    return None


def recover_stale_jobs(max_age_seconds: float | None = None) -> int:
    """
    Reset jobs stuck in 'working' or 'claimed' status back to 'queued'.

    This handles jobs that were interrupted by crashes or restarts.
    Returns number of recovered jobs.
    """
    if max_age_seconds is None:
        max_age_seconds = cfg.STALE_JOB_TIMEOUT

    cutoff = time.time() - max_age_seconds
    with db.connection_context():
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


def cleanup_old_jobs(retention_hours: int | None = None) -> tuple[int, int]:
    """
    Delete completed jobs older than retention_hours and their HLS directories.

    Returns (jobs_deleted, dirs_deleted).
    """
    if retention_hours is None:
        retention_hours = cfg.JOB_RETENTION_HOURS

    cutoff = time.time() - (retention_hours * 3600)

    with db.connection_context():
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


def get_queue_stats() -> dict[str, int]:
    """Get counts of jobs by status for health checks."""
    with db.connection_context():
        queued = Job.select().where(Job.status == "queued").count()
        working = Job.select().where(Job.status.in_(["working", "claimed"])).count()
        done = Job.select().where(Job.status == "done").count()
        cancelled = Job.select().where(Job.status == "cancelled").count()
        errors = Job.select().where(Job.status.startswith("error")).count()

    return {
        "queued": queued,
        "working": working,
        "done": done,
        "cancelled": cancelled,
        "errors": errors,
    }


# Initialize database on module import
init_db()

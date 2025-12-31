"""
models.py – Peewee ORM models for storing transcoding job metadata in SQLite.

The Job model stores all job state including transcode parameters as JSON.
Queue functionality is implemented via status field polling.
"""
from __future__ import annotations

import logging
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

log = logging.getLogger(__name__)

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
    retry_count = FloatField(default=0)  # number of retry attempts
    media_info_json = TextField(default="{}")  # JSON-serialized MediaInfo

    class Meta:
        table_name = "jobs"


def init_db() -> None:
    """Create tables if they don't exist, and migrate schema if needed."""
    log.debug("[DB_INIT] initializing database at %s", cfg.DATABASE_PATH)
    try:
        with db.connection_context():
            db.create_tables([Job], safe=True)
            log.debug("[DB_INIT] tables created/verified")

            # Migration: add retry_count column if missing (for existing databases)
            cursor = db.execute_sql("PRAGMA table_info(jobs)")
            columns = {row[1] for row in cursor.fetchall()}
            log.debug("[DB_INIT] existing columns: %s", columns)

            if "retry_count" not in columns:
                log.info("[DB_INIT] migrating: adding retry_count column")
                db.execute_sql("ALTER TABLE jobs ADD COLUMN retry_count REAL DEFAULT 0")
                log.debug("[DB_INIT] migration complete")

            if "media_info_json" not in columns:
                log.info("[DB_INIT] migrating: adding media_info_json column")
                db.execute_sql("ALTER TABLE jobs ADD COLUMN media_info_json TEXT DEFAULT '{}'")
                log.debug("[DB_INIT] migration complete")

        log.debug("[DB_INIT] database initialization complete")
    except Exception as e:
        log.error("[DB_INIT] failed to initialize database: %s", e, exc_info=True)
        raise


def claim_next_queued_job() -> Job | None:
    """
    Atomically claim the next queued job by updating its status to 'claimed'.

    Returns the Job if one was claimed, None if queue is empty.
    Uses a transaction to prevent race conditions between workers.
    """
    log.debug("[QUEUE] attempting to claim next job")
    try:
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
                    log.info("[QUEUE] claimed job %s (src=%s)", job.job_id, Path(job.src).name)
                    return job
        log.debug("[QUEUE] no jobs in queue")
        return None
    except Exception as e:
        log.error("[QUEUE] failed to claim job: %s", e, exc_info=True)
        raise


def recover_stale_jobs(max_age_seconds: float | None = None) -> int:
    """
    Reset jobs stuck in 'working' or 'claimed' status back to 'queued'.

    This handles jobs that were interrupted by crashes or restarts.
    Returns number of recovered jobs.
    """
    if max_age_seconds is None:
        max_age_seconds = cfg.STALE_JOB_TIMEOUT

    log.debug("[RECOVERY] checking for stale jobs (max_age=%ds)", max_age_seconds)
    cutoff = time.time() - max_age_seconds

    try:
        with db.connection_context():
            # First, log what we're about to recover
            stale_jobs = list(
                Job.select(Job.job_id, Job.status, Job.started)
                .where(
                    (Job.status.in_(["working", "claimed"]))
                    & (Job.started < cutoff)
                )
            )
            if stale_jobs:
                for j in stale_jobs:
                    age = time.time() - j.started
                    log.debug("[RECOVERY] found stale job %s (status=%s, age=%.0fs)",
                              j.job_id, j.status, age)

            with db.atomic():
                count = (
                    Job.update(status="queued")
                    .where(
                        (Job.status.in_(["working", "claimed"]))
                        & (Job.started < cutoff)
                    )
                    .execute()
                )
        if count:
            log.info("[RECOVERY] recovered %d stale jobs", count)
        else:
            log.debug("[RECOVERY] no stale jobs found")
        return count
    except Exception as e:
        log.error("[RECOVERY] failed: %s", e, exc_info=True)
        raise


def cleanup_old_jobs(retention_hours: int | None = None) -> tuple[int, int]:
    """
    Delete completed jobs older than retention_hours and their HLS directories.

    Returns (jobs_deleted, dirs_deleted).
    """
    if retention_hours is None:
        retention_hours = cfg.JOB_RETENTION_HOURS

    log.debug("[CLEANUP] checking for old jobs (retention=%d hours)", retention_hours)
    cutoff = time.time() - (retention_hours * 3600)

    try:
        with db.connection_context():
            old_jobs = list(
                Job.select(Job.job_id)
                .where((Job.status == "done") & (Job.started < cutoff))
            )

            if old_jobs:
                log.debug("[CLEANUP] found %d old jobs to clean", len(old_jobs))

            dirs_deleted = 0
            for job in old_jobs:
                hls_dir = cfg.HLS_DIR / job.job_id
                if hls_dir.exists():
                    log.debug("[CLEANUP] removing HLS directory: %s", hls_dir)
                    shutil.rmtree(hls_dir, ignore_errors=True)
                    dirs_deleted += 1

            jobs_deleted = (
                Job.delete()
                .where((Job.status == "done") & (Job.started < cutoff))
                .execute()
            )

        if jobs_deleted:
            log.info("[CLEANUP] deleted %d jobs, %d directories", jobs_deleted, dirs_deleted)
        else:
            log.debug("[CLEANUP] nothing to clean")
        return jobs_deleted, dirs_deleted
    except Exception as e:
        log.error("[CLEANUP] failed: %s", e, exc_info=True)
        raise


def get_queue_stats() -> dict[str, int]:
    """Get counts of jobs by status for health checks."""
    log.debug("[STATS] getting queue statistics")
    try:
        with db.connection_context():
            queued = Job.select().where(Job.status == "queued").count()
            working = Job.select().where(Job.status.in_(["working", "claimed"])).count()
            done = Job.select().where(Job.status == "done").count()
            cancelled = Job.select().where(Job.status == "cancelled").count()
            errors = Job.select().where(Job.status.startswith("error")).count()

        stats = {
            "queued": queued,
            "working": working,
            "done": done,
            "cancelled": cancelled,
            "errors": errors,
        }
        log.debug("[STATS] queue stats: %s", stats)
        return stats
    except Exception as e:
        log.error("[STATS] failed to get stats: %s", e, exc_info=True)
        raise


# Initialize database on module import
init_db()

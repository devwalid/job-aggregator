from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from typing import Optional
from adapters.remoteok import fetch_remoteok_jobs
from adapters.remotive import fetch_remotive_jobs
from core.util import retry_async
import asyncio
import logging

from core.db import SessionLocal
from core.crud import upsert_job
from adapters.hn import fetch_hn_jobs

scheduler: Optional[AsyncIOScheduler] = None


async def collect_hn_once():
    db: Session = SessionLocal()
    try:
        items = await fetch_hn_jobs()
        log = logging.getLogger("job-aggregator.adapters")
        log.info("Fetched %s items from HN", len(items))
        for item in items:
            upsert_job(db, item)
        db.commit()
    finally:
        db.close()

async def collect_remoteok_once():
    from core.db import SessionLocal
    from core.crud import upsert_job
    db = SessionLocal()
    try:
        items = await retry_async(fetch_remoteok_jobs, attempts=3, delay=1.0)
        for item in items:
            upsert_job(db, item)
        db.commit()
    finally:
        db.close()

async def collect_remotive_once():
    from core.db import SessionLocal
    from core.crud import upsert_job
    db = SessionLocal()
    try:
        items = await retry_async(lambda: fetch_remotive_jobs(search=None), attempts=3, delay=1.0)
        for item in items:
            upsert_job(db, item)
        db.commit()
    finally:
        db.close()

def start_scheduler():
    global scheduler
    if scheduler:
        return scheduler
    scheduler = AsyncIOScheduler()

    scheduler.add_job(lambda: asyncio.create_task(collect_hn_once()),
                      "interval", hours=1, id="collect_hn")
    scheduler.add_job(lambda: asyncio.create_task(collect_remoteok_once()),
                      "interval", hours=1, id="collect_remoteok")
    scheduler.add_job(lambda: asyncio.create_task(collect_remotive_once()),
                      "interval", hours=1, id="collect_remotive")
    scheduler.start()
    return scheduler

def shutdown_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown(wait=False)
        scheduler = None
                    
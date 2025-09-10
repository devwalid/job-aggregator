from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from typing import Optional
import asyncio

from core.db import SessionLocal
from core.crud import upsert_job
from adapters.hn import fetch_hn_jobs

scheduler: Optional[AsyncIOScheduler] = None

async def collect_hn_once():
    db: Session = SessionLocal()
    try:
        items = await fetch_hn_jobs()
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
    scheduler.start()
    return scheduler

def shutdown_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown(wait=False)
        scheduler = None
                    
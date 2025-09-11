from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime
from core.logging import setup_logging

from core.db import get_db
from core import models, schemas

router = APIRouter(prefix="/jobs", tags=["jobs"])
logger = setup_logging()
logger.info("API starting...")


@router.get("/", response_model=List[schemas.JobSchema])
def list_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    q: str = "",
    source: Optional[str] = Query(None, description="Filter by source, e.g. hn, indeed"),
    status: Optional[str] = Query(None, description="Filter by status: NEW|SAVED|APPLIED"),
    from_date: Optional[str] = Query(None, description="ISO date, e.g. 2025-09-01"),
    to_date: Optional[str] = Query(None, description="ISO date, e.g. 2025-09-08"),
):
    query = db.query(models.Job)

    if q:
        terms = [t.strip() for t in q.split() if t.strip()]
        for term in terms:
            like = f"%{term}%"
            query = query.filter(
                or_(
                    models.Job.title.ilike(like),
                    models.Job.company.ilike(like),
                    models.Job.location.ilike(like),
                )
            )
    if source:
        query = query.filter(models.Job.source == source)
    if status:
        query = query.filter(models.Job.status == status)

    if from_date:
        try:
            dt = datetime.fromisoformat(from_date)
            query = query.filter(models.Job.posted_at >= dt)
        except ValueError:
            pass
    if to_date:
        try:
            dt = datetime.fromisoformat(to_date)
            query = query.filter(models.Job.posted_at <= dt)
        except ValueError:
            pass
    
    return query.offset(skip).limit(min(limit, 200)).all()

@router.post("/collect/run")
async def collect_now(db: Session = Depends(get_db)):
    from adapters.hn import fetch_hn_jobs
    from core.crud import upsert_job

    # Step 1: fetch from API
    try:
        items = await fetch_hn_jobs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"fetch_hn_jobs failed: {e}")
    
    if items is None:
        raise HTTPException(status_code=500, detail="fetch_hn_jobs returned None")
    

    try:
        count = 0
        for item in items:
            upsert_job(db, item)
            count += 1
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB upsert failed: {e}")
    
    return {"inserted_or_updated": count}

@router.post("/collect/all")
async def collect_all(db: Session = Depends(get_db)):
    from core.crud import upsert_job
    from core.util import retry_async
    from adapters.hn import fetch_hn_jobs

    total = 0
    for fn in (fetch_hn_jobs,):
        items = await retry_async(fn, attempts=3, delay=1.0)
        for it in items:
            upsert_job(db, it)
            total += 1
        db.commit()
        return {"inserted_or_updated": total}
    
@router.post("/collect/remotive")
async def collect_remotive(db: Session = Depends(get_db)):
    from adapters.remotive import fetch_remotive_jobs
    from core.crud import upsert_job
    from core.util import retry_async

    try:
        items = await retry_async(lambda: fetch_remotive_jobs(search=None), attempts=3, delay=1.0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"fetch_remotive_jobs failed: {e}")
    
    try:
        count = 0
        for item in items:
            upsert_job(db, item)
            count += 1
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB upsert failed: {e}")
    
    return {"inserted_or_updated": count}


@router.get("/last_refresh")
def last_refresh(db: Session = Depends(get_db)):
    last_dt, total = db.query(
        func.max(models.Job.fetched_at),
        func.count(models.Job.id),
    ).one()
    return {
        "last_refresh": last_dt.isoformat() if last_dt else None,
        "total": int(total or 0),
    }
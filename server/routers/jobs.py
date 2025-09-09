from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime

from core.db import get_db
from core import models, schemas

router = APIRouter(prefix="/jobs", tags=["jobs"])

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
        like = f"%{q}"
        query = query.filter(
            (models.Job.title.ilike(like)) |
            (models.Job.company.ilike(like)) |
            (models.Job.location.ilike(like))
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
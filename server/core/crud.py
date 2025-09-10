from sqlalchemy.orm import Session
from typing import Dict, Any
import uuid
from datetime import datetime

from core.models import Job

def upsert_job(db: Session, payload: Dict[str, Any]) -> Job:
    """Upsert by (source, externa_id). If not found, insert. Returns the Job."""
    source = payload.get("source")
    external_id = payload.get("external_id")

    q = db.query(Job).filter(Job.source == source, Job.external_id == external_id)
    inst = q.first()
    if inst:
        inst.title = payload.get("title", inst.title)
        inst.company = payload.get("company", inst.company)
        inst.location = payload.get("location", inst.location)
        inst.url = payload.get("url", inst.url)
        inst.posted_at = payload.get("posted_at", inst.posted_at)
        inst.status = payload.get("status", inst.status)
        inst.fetched_at = datetime.utcnow()
    else:
        inst = Job(
            id=str(uuid.uuid4()),
            source=source,
            external_id=external_id,
            title=payload.get("title"),
            company=payload.get("company"),
            location=payload.get("location"),
            url=payload.get("url"),
            posted_at=payload.get("posted_at"),
            status=payload.get("status", "NEW"),
            fetched_at=datetime.utcnow(),
        )
        db.add(inst)
    return inst
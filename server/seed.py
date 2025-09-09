import uuid
from datetime import datetime, timedelta
from core.db import SessionLocal, Base, engine
from core.models import Job

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Job).delete()

now= datetime.utcnow()

seed_rows = [
    Job(
        id=str(uuid.uuid4()),
        source="hn",
        external_id="hn-42001",
        title="Junior Python Developer (FastAPI)",
        company="Acme Labs",
        location="Remote",
        url="https://news.ycombinator.com/item?id=42001",
        posted_at=now - timedelta(days=1),
        status="NEW",
    ),
    Job(
        id=str(uuid.uuid4()),
        source="indeed",
        external_id="ind-88877",
        title="React Frontend Engineer (Entry Level)",
        company="BrightSoft",
        location="Casablanca",
        url="https://indeed.com/viewjob?jk=88877",
        posted_at=now - timedelta(days=2),
        status="SAVED",
    ),
    Job(
        id=str(uuid.uuid4()),
        source="hn",
        external_id="hn-42002",
        title="Automation Engineer (playwright)",
        company="Orbit Systems",
        location="Remote",
        url="https://news.ycombinator.com/item?id=42002",
        posted_at=now - timedelta(days=3),
        status="APPLIED",
    ),
]

db.add_all(seed_rows)
db.commit()
db.close()
print("✅ Seeded jobs")
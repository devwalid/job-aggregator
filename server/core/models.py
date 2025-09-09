from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from core.db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    source = Column(String, index=True)
    external_id = Column(String, index=True)
    title = Column(String, index=True)
    company = Column(String, nullable=True, index=True)
    location = Column(String, nullable=True, index=True)
    url = Column(String)
    posted_at = Column(DateTime, nullable=True, index=True)
    fetched_at = Column(DateTime, server_default=func.now(), index=True)
    status = Column(String, default="NEW", index=True)
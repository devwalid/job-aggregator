from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobSchema(BaseModel):
    id: str
    source: str
    external_id: Optional[str] = None
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    url: str
    posted_at: Optional[datetime] = None
    fetched_at: datetime
    status: str

    class Config:
        orm_mode = True
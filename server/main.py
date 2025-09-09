from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db import Base, engine
from core.settings import CORS_ORIGINS, DATABASE_URL
from routers import jobs

# tables (simple for M1; switch to almebic later)
Base.metadata.create_all(bind=engine)

app= FastAPI(title="Job Aggregator API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)

@app.get("/health")
def health():
    return{"status": "ok"}


print(f"Using DATABASE_URL: {DATABASE_URL}")
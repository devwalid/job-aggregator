import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB = f"sqlite:///{(BASE_DIR / 'jobs.db').as_posix()}"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)

CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
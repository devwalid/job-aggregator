# Job Aggregator

FastAPI + React monorepo. Collects jobs from multiple sources and shows them in a polished dashboard.

## Run backend
```bash
cd server
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
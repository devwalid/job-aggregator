from typing import List, Dict, Any
from datetime import datetime
import httpx

REMOTIVE_API = "https://remotive.com/api/remote-jobs"

def _parse_dt(s: str | None):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None
    
async def fetch_remotive_jobs(category: str | None = None, search: str | None = None) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {}
    if category:
        params["category"] = category
    if search:
        params["search"] = search

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(REMOTIVE_API, params=params)
        r.raise_for_status()
        data = r.json()

    results: List[Dict[str, Any]] = []
    for j in data.get("jobs", []):
        results.append({
            "external_id": f"remotive-{j.get('id')}",
            "title": j.get("title"),
            "url": j.get("url"),
            "posted_at": _parse_dt(j.get("publication_date")),
            "company": j.get("company_name"),
            "location": j.get("candidate_required_location") or j.get("job_type"),
            "source": "remotive",
            "status": "NEW",
        })
    return results
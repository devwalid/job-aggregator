# server/adapters/hn.py
# Real data: Hacker News Algolia "jobstory"
from typing import List, Dict, Any
import httpx
from datetime import datetime

ALGOLIA_JOBS_URL = "https://hn.algolia.com/api/v1/search_by_date?tags=jobstory"

async def fetch_hn_jobs(query: str | None = None, page: int = 0) -> List[Dict[str, Any]]:
    params = {"page": page}
    if query:
        params["query"] = query

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(ALGOLIA_JOBS_URL, params=params)
        r.raise_for_status()
        data = r.json()

    results: List[Dict[str, Any]] = []
    for hit in data.get("hits", []):
        created = hit.get("created_at")  # e.g. "2025-09-10T11:35:01.000Z"
        posted_at = datetime.fromisoformat(created.replace("Z", "+00:00")) if created else None

        results.append({
            "external_id": hit.get("objectID"),
            "title": hit.get("title") or hit.get("story_title") or "HN Job",
            "url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "posted_at": posted_at,
            "company": None,
            "location": None,
            "source": "hn",
            "status": "NEW",
        })

    return results  # ← important: must be outside the loop
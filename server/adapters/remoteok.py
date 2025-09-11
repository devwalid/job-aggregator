from typing import List, Dict, Any
from playwright.async_api import async_playwright, TimeoutError as PWTimeout
import asyncio

REMOTEOK_URL = "https://remoteok.com/remote-dev-jobs"

async def fetch_remoteok_jobs() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu",
            ],
        )
        ctx = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        # Hide webdriver flag
        await ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Block heavy resources to speed up/avoid timeouts
        async def route_handler(route):
            req = route.request
            if req.resource_type in {"image", "media", "font"}:
                await route.abort()
            else:
                await route.continue_()
        await ctx.route("**/*", route_handler)

        page = await ctx.new_page()

        try:
            # Looser wait; don't require networkidle
            await page.goto(REMOTEOK_URL, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_selector("tr.job", timeout=60000)
        except PWTimeout:
            await ctx.close()
            await browser.close()
            # surface a clearer error for the API layer
            raise RuntimeError("RemoteOK: initial load timeout")

        rows = await page.locator("tr.job").all()
        for r in rows:
            job_id = await r.get_attribute("data-id")
            # Title
            title = await r.locator("td.company_and_position h2").first.text_content()
            title = (title or "").strip() if title else ""
            # URL (pick first link)
            href = await r.locator("a.preventLink").first.get_attribute("href")
            if href and href.startswith("/"):
                url = f"https://remoteok.com{href}"
            else:
                url = href or REMOTEOK_URL
            # Company
            company = None
            el = r.locator("td.company_and_position .companyLink h3").first
            if await el.count() > 0:
                txt = await el.text_content()
                company = (txt or "").strip() or None
            # Location
            location = None
            lel = r.locator("div.location").first
            if await lel.count() > 0:
                txt = await lel.text_content()
                location = (txt or "").strip() or None

            if not (job_id and title and url):
                continue

            results.append({
                "external_id": f"rok-{job_id}",
                "title": title,
                "url": url,
                "posted_at": None,
                "company": company,
                "location": location,
                "source": "remoteok",
                "status": "NEW",
            })

        await ctx.close()
        await browser.close()

    return results
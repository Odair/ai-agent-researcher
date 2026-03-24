import asyncio

import httpx
import trafilatura

from app.schemas import ScrapedResult, SearchResult

from playwright.async_api import async_playwright

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
_TIMEOUT = 10


async def _fetch_with_playwright(url: str) -> str | None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=15000, wait_until="domcontentloaded")
            html = await page.content()
            return trafilatura.extract(html, include_comments=False, include_tables=False)
        except Exception:
            return None
        finally:
            await browser.close()


async def _fetch_one(client: httpx.AsyncClient, result: SearchResult) -> ScrapedResult:
    try:
        response = await client.get(result.url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        response.raise_for_status()
        extracted = trafilatura.extract(response.text, include_comments=False, include_tables=False)
        if extracted:
            return ScrapedResult(**result.model_dump(), full_content=extracted, scraped=True)
    except Exception:
        pass

    extracted = await _fetch_with_playwright(result.url)
    if extracted:
        return ScrapedResult(**result.model_dump(), full_content=extracted, scraped=True)

    return ScrapedResult(**result.model_dump(), full_content=result.content, scraped=False)


async def scrape(results: list[SearchResult]) -> list[ScrapedResult]:
    async with httpx.AsyncClient() as client:
        tasks = [_fetch_one(client, r) for r in results]
        return await asyncio.gather(*tasks)

import asyncio

import httpx
import trafilatura

from app.schemas import ScrapedResult, SearchResult

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
_TIMEOUT = 10


async def _fetch_one(client: httpx.AsyncClient, result: SearchResult) -> ScrapedResult:
    try:
        response = await client.get(result.url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        response.raise_for_status()
        extracted = trafilatura.extract(response.text, include_comments=False, include_tables=False)
        full_content = extracted or result.content
    except Exception:
        full_content = result.content

    return ScrapedResult(**result.model_dump(), full_content=full_content)


async def scrape(results: list[SearchResult]) -> list[ScrapedResult]:
    async with httpx.AsyncClient() as client:
        tasks = [_fetch_one(client, r) for r in results]
        return await asyncio.gather(*tasks)

import asyncio
import json

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from app.schemas import SearchResult
from app.services import scraper as scraper_service


class ScrapeToolInput(BaseModel):
    results_json: str = Field(
        description="JSON string com lista de resultados de busca (cada item com title, url, content)"
    )


class ScrapeTool(BaseTool):
    name: str = "scrape_article_content"
    description: str = (
        "Faz scraping do conteúdo completo dos artigos a partir de uma lista de resultados de busca. "
        "Recebe um JSON string com a lista e retorna o conteúdo completo de cada URL."
    )
    args_schema: type[BaseModel] = ScrapeToolInput

    def _run(self, results_json: str) -> str:
        raw = json.loads(results_json)
        results = [SearchResult(**r) for r in raw]
        scraped = asyncio.run(scraper_service.scrape(results))
        return json.dumps([r.model_dump() for r in scraped], ensure_ascii=False)

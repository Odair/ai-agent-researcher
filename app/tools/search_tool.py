import asyncio
import json

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from app.schemas import SearchRequest
from app.services import search as search_service


class SearchToolInput(BaseModel):
    query: str = Field(description="Nome da empresa ou ticker da B3 (ex: PETR4, Petrobras)")


class SearchTool(BaseTool):
    name: str = "search_financial_news"
    description: str = (
        "Busca notícias financeiras de uma empresa ou ticker da B3. "
        "Retorna uma lista de resultados com título, URL e snippet."
    )
    args_schema: type[BaseModel] = SearchToolInput

    def _run(self, query: str) -> str:
        request = SearchRequest(s=query)
        result = asyncio.run(search_service.search(request))
        data = result.get("data", [])
        return json.dumps(data, ensure_ascii=False)

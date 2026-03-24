import json

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from app.schemas import ScrapedResult
from app.services import classifier as classifier_service


class ClassifyToolInput(BaseModel):
    results_json: str = Field(
        description="JSON string com lista de artigos raspados (cada item com title, url, content, full_content)"
    )


class ClassifyTool(BaseTool):
    name: str = "classify_news_sentiment"
    description: str = (
        "Classifica notícias financeiras como 'positive', 'negative' ou 'noise' "
        "para análise de ações da B3. Retorna cada item com sentiment e razão."
    )
    args_schema: type[BaseModel] = ClassifyToolInput

    def _run(self, results_json: str) -> str:
        raw = json.loads(results_json)
        results = [ScrapedResult(**r) for r in raw]
        classified = classifier_service.classify(results)
        return json.dumps([r.model_dump() for r in classified], ensure_ascii=False)

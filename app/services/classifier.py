import json

import anthropic
from fastapi import HTTPException

from app.config import ANTHROPIC_API_KEY
from app.schemas import ClassifiedResult, ScrapedResult

_MODEL = "claude-haiku-4-5-20251001"

_SYSTEM_PROMPT = """\
Você é um analista financeiro especializado no mercado de ações brasileiro (B3).
Analise cada notícia e classifique seu impacto para o investidor da ação em questão:

- "positive": notícia com impacto positivo direto (resultados acima do esperado, expansão, dividendos, upgrades, contratos relevantes, etc.)
- "negative": notícia com impacto negativo direto (resultados abaixo do esperado, investigações, rebaixamentos, queda de receita, etc.)
- "noise": sem conteúdo jornalístico relevante (página de cotação, descrição genérica da empresa, tutorial, dado histórico sem notícia nova, etc.)

Responda APENAS com um array JSON no formato:
[{"sentiment": "positive"|"negative"|"noise", "reason": "<justificativa em até 20 palavras>"}, ...]

A ordem deve corresponder exatamente à lista de entrada.\
"""


def classify(results: list[ScrapedResult]) -> list[ClassifiedResult]:
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    items = [
        {"title": r.title, "content": r.full_content[:2000]}
        for r in results
    ]
    user_message = json.dumps(items, ensure_ascii=False)

    response = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()
    # strip markdown code block if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    classifications: list[dict] = json.loads(raw)

    classified = []
    for result, cls in zip(results, classifications):
        classified.append(
            ClassifiedResult(
                **result.model_dump(),
                sentiment=cls["sentiment"],
                reason=cls["reason"],
            )
        )

    return classified

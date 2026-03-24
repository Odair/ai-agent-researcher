from fastapi import FastAPI

from app.schemas import SearchRequest
from app.services import search as search_service

app = FastAPI(title="AI Agent Researcher", version="0.1.0")


@app.post("/search")
async def search(request: SearchRequest) -> dict:
    return await search_service.search(request)

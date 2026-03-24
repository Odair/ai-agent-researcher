import httpx
from fastapi import HTTPException

from app.config import SEARCHCANS_API_KEY, SEARCHCANS_BASE_URL
from app.schemas import SearchRequest


async def search(request: SearchRequest) -> dict:
    if not SEARCHCANS_API_KEY:
        raise HTTPException(status_code=500, detail="SEARCHCANS_API_KEY not configured")

    headers = {
        "Authorization": f"Bearer {SEARCHCANS_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SEARCHCANS_BASE_URL}/search",
            headers=headers,
            json=request.model_dump(),
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

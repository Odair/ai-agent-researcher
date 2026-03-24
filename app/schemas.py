from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    s: str = Field(..., description="Search query")
    t: str = Field(default="google", description="Search engine (e.g. 'google')")
    p: int = Field(default=1, ge=1, description="Page number")


class SearchResponse(BaseModel):
    data: dict

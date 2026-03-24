from typing import Literal

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    s: str = Field(..., description="Search query")
    t: str = Field(default="google", description="Search engine (e.g. 'google')")
    p: int = Field(default=1, ge=1, description="Page number")


class SearchResponse(BaseModel):
    data: dict


class SearchResult(BaseModel):
    title: str
    url: str
    content: str


class ScrapedResult(SearchResult):
    full_content: str
    scraped: bool


class ClassifiedResult(ScrapedResult):
    sentiment: Literal["positive", "negative", "noise"]
    reason: str

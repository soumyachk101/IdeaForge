"""Pydantic request/response models for the API."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GenerateRequest(BaseModel):
    niche: str = Field(default="general", description="Target niche for idea generation")


class TrendResponse(BaseModel):
    source: str
    title: str
    description: str
    url: str
    upvotes: int = 0
    comments: List[str] = []
    comments_count: int = 0
    tags: List[str] = []
    scraped_at: Optional[datetime] = None

    def model_post_init(self, __context):
        if self.comments_count == 0 and self.comments:
            self.comments_count = len(self.comments)


class RAGQueryRequest(BaseModel):
    query: str
    collection: str = "all"
    n_results: int = 5


class RAGQueryResponse(BaseModel):
    results: dict


class HealthResponse(BaseModel):
    status: str
    version: str
    llm_provider: str
    chroma_status: str


class StatsResponse(BaseModel):
    pain_points_count: int
    monetization_frameworks_count: int
    startup_case_studies_count: int
    generated_ideas_count: int

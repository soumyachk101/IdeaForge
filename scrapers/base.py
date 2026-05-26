"""Base scraper and TrendData model."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from abc import ABC, abstractmethod


class TrendData(BaseModel):
    """Standardized trend data from any source."""
    source: str
    title: str
    description: str
    url: str
    upvotes: int = 0
    comments: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

    def to_context_text(self) -> str:
        """Converts to text for RAG context."""
        comments_text = "\n".join(f"- {c}" for c in self.comments[:10]) if self.comments else "No comments"
        tags_text = ", ".join(self.tags) if self.tags else "None"
        return (
            f"[{self.source.upper()}] {self.title}\n"
            f"Description: {self.description}\n"
            f"Upvotes: {self.upvotes}\n"
            f"Tags: {tags_text}\n"
            f"User Comments:\n{comments_text}"
        )


class BaseScraper(ABC):
    """Base class for all scrapers."""

    @abstractmethod
    async def scrape(self, limit: int = 20) -> List[TrendData]:
        """Scrape trends from the source."""
        ...

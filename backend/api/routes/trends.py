"""Trend scraping endpoints."""
import logging
from fastapi import APIRouter
from typing import List

from api.models import TrendResponse
from scrapers.hacker_news import HackerNewsScraper
from scrapers.reddit import RedditScraper
from scrapers.product_hunt import ProductHuntScraper
from scrapers.indie_hackers import IndieHackersScraper
from config import CONFIG

router = APIRouter()
logger = logging.getLogger("ideaforge.api.trends")

_trends_cache: dict = {}


@router.get("/trends", response_model=List[TrendResponse])
async def get_trends(source: str = "all", limit: int = 20):
    """Get cached trends."""
    if source == "all":
        all_trends = []
        for trends in _trends_cache.values():
            all_trends.extend(trends)
        return all_trends[:limit]
    return _trends_cache.get(source, [])[:limit]


@router.post("/trends/scrape")
async def scrape_trends(source: str = "all", limit: int = 20):
    """Trigger a fresh scrape from all sources."""
    scrapers = _get_scrapers(source)
    scraped_sources = []

    for name, scraper in scrapers.items():
        try:
            trends = await scraper.scrape(limit=limit)
            _trends_cache[name] = [
                TrendResponse(**t.model_dump()) for t in trends
            ]
            scraped_sources.append(name)
        except Exception as e:
            logger.error(f"Scraping {name} failed: {e}")

    return {"message": f"Scraped {len(scraped_sources)} sources", "sources": scraped_sources}


def _get_scrapers(source: str) -> dict:
    all_scrapers = {
        "hacker_news": HackerNewsScraper(),
        "reddit": RedditScraper(),
        "product_hunt": ProductHuntScraper(),
        "indie_hackers": IndieHackersScraper(),
    }
    if source == "all":
        return all_scrapers
    if source in all_scrapers:
        return {source: all_scrapers[source]}
    return {}

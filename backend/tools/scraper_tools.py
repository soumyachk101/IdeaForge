"""CrewAI tools wrapping the scrapers."""
import asyncio
import json
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


def _run_async(coro):
    """Run async function safely from sync context, even inside existing event loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result(timeout=120)
    else:
        return asyncio.run(coro)


class ScrapeProductHuntInput(BaseModel):
    limit: int = Field(default=10, description="Number of products to scrape")


class ScrapeProductHuntTool(BaseTool):
    name: str = "scrape_product_hunt"
    description: str = "Scrapes today's top Product Hunt launches with descriptions, upvotes, and user comments."
    args_schema: Type[BaseModel] = ScrapeProductHuntInput

    def _run(self, limit: int = 10) -> str:
        from scrapers.product_hunt import ProductHuntScraper
        scraper = ProductHuntScraper()
        results = _run_async(scraper.scrape(limit=limit))
        return json.dumps([r.model_dump(mode="json") for r in results], indent=2)


class ScrapeHackerNewsInput(BaseModel):
    limit: int = Field(default=10, description="Number of stories to scrape")


class ScrapeHackerNewsTool(BaseTool):
    name: str = "scrape_hacker_news"
    description: str = "Scrapes top Hacker News stories with comments. Best for finding tech trends and developer tools."
    args_schema: Type[BaseModel] = ScrapeHackerNewsInput

    def _run(self, limit: int = 10) -> str:
        from scrapers.hacker_news import HackerNewsScraper
        scraper = HackerNewsScraper()
        results = _run_async(scraper.scrape(limit=limit))
        return json.dumps([r.model_dump(mode="json") for r in results], indent=2)


class ScrapeRedditInput(BaseModel):
    limit: int = Field(default=10, description="Number of posts to scrape")


class ScrapeRedditTool(BaseTool):
    name: str = "scrape_reddit_saas"
    description: str = "Scrapes Reddit SaaS/microsaas subreddits for user complaints, pain points, and business ideas."
    args_schema: Type[BaseModel] = ScrapeRedditInput

    def _run(self, limit: int = 10) -> str:
        from scrapers.reddit import RedditScraper
        scraper = RedditScraper()
        results = _run_async(scraper.scrape(limit=limit))
        return json.dumps([r.model_dump(mode="json") for r in results], indent=2)


class ScrapeIndieHackersInput(BaseModel):
    limit: int = Field(default=10, description="Number of posts to scrape")


class ScrapeIndieHackersTool(BaseTool):
    name: str = "scrape_indie_hackers"
    description: str = "Scrapes Indie Hackers for trending posts about bootstrapped businesses and monetization."
    args_schema: Type[BaseModel] = ScrapeIndieHackersInput

    def _run(self, limit: int = 10) -> str:
        from scrapers.indie_hackers import IndieHackersScraper
        scraper = IndieHackersScraper()
        results = _run_async(scraper.scrape(limit=limit))
        return json.dumps([r.model_dump(mode="json") for r in results], indent=2)

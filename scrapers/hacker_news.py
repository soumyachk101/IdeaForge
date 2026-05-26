"""Hacker News scraper using the Firebase API."""
import httpx
import asyncio
import logging
from typing import List

from scrapers.base import BaseScraper, TrendData

logger = logging.getLogger("ideaforge.scrapers.hn")

HN_API = "https://hacker-news.firebaseio.com/v0"


class HackerNewsScraper(BaseScraper):
    async def scrape(self, limit: int = 20) -> List[TrendData]:
        """Scrapes top stories from Hacker News."""
        trends = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get top story IDs
            resp = await client.get(f"{HN_API}/topstories.json")
            if resp.status_code != 200:
                logger.error(f"HN API returned {resp.status_code}")
                return []

            story_ids = resp.json()[:limit]

            # Fetch each story in parallel
            tasks = [self._fetch_story(client, sid) for sid in story_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, TrendData):
                    trends.append(result)
                elif isinstance(result, Exception):
                    logger.warning(f"Failed to fetch story: {result}")

        logger.info(f"Scraped {len(trends)} stories from Hacker News")
        return trends

    async def _fetch_story(self, client: httpx.AsyncClient, story_id: int) -> TrendData:
        """Fetches a single story and its comments."""
        resp = await client.get(f"{HN_API}/item/{story_id}.json")
        data = resp.json()

        if not data or data.get("type") != "story":
            raise ValueError(f"Item {story_id} is not a story")

        # Fetch top comments
        comments = []
        comment_ids = data.get("kids", [])[:5]
        for cid in comment_ids:
            try:
                cresp = await client.get(f"{HN_API}/item/{cid}.json")
                cdata = cresp.json()
                if cdata and cdata.get("text"):
                    # Strip HTML tags simply
                    text = cdata["text"].replace("<p>", " ").replace("</p>", "")
                    comments.append(text[:300])
            except Exception:
                pass

        tags = []
        title_lower = data.get("title", "").lower()
        if "show hn" in title_lower:
            tags.append("show-hn")
        if "ask hn" in title_lower:
            tags.append("ask-hn")

        return TrendData(
            source="hacker_news",
            title=data.get("title", ""),
            description=data.get("text", "")[:500] if data.get("text") else "",
            url=data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
            upvotes=data.get("score", 0),
            comments=comments,
            tags=tags,
        )

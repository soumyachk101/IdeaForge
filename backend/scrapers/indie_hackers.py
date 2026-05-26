"""Indie Hackers scraper."""
import httpx
import logging
from typing import List
from bs4 import BeautifulSoup

from scrapers.base import BaseScraper, TrendData

logger = logging.getLogger("ideaforge.scrapers.ih")


class IndieHackersScraper(BaseScraper):
    async def scrape(self, limit: int = 20) -> List[TrendData]:
        """Scrapes trending posts from Indie Hackers."""
        trends = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.get(
                    "https://www.indiehackers.com/",
                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
                )

                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")

                    # Find post links
                    post_links = soup.find_all("a", href=lambda h: h and "/post/" in h)
                    seen_urls = set()

                    for link in post_links[:limit * 2]:
                        href = link.get("href", "")
                        if href in seen_urls:
                            continue
                        seen_urls.add(href)

                        title = link.get_text(strip=True)
                        if not title or len(title) < 5:
                            continue

                        full_url = f"https://www.indiehackers.com{href}" if href.startswith("/") else href

                        trends.append(TrendData(
                            source="indie_hackers",
                            title=title[:200],
                            description="",
                            url=full_url,
                            upvotes=0,
                            comments=[],
                            tags=["indie-hackers"],
                        ))

                        if len(trends) >= limit:
                            break

                else:
                    logger.warning(f"Indie Hackers returned {resp.status_code}")

            except Exception as e:
                logger.error(f"Failed to scrape Indie Hackers: {e}")

        logger.info(f"Scraped {len(trends)} posts from Indie Hackers")
        return trends

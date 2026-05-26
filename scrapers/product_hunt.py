"""Product Hunt scraper using their API."""
import httpx
import logging
from datetime import datetime
from typing import List

from scrapers.base import BaseScraper, TrendData
from config import CONFIG

logger = logging.getLogger("ideaforge.scrapers.ph")


class ProductHuntScraper(BaseScraper):
    async def scrape(self, limit: int = 20) -> List[TrendData]:
        """Scrapes today's top Product Hunt launches."""
        trends = []
        token = CONFIG.get("product_hunt_token", "")

        if not token:
            logger.warning("No Product Hunt token configured, using public API")
            return await self._scrape_public(limit)

        # GraphQL API
        query = """
        query {
            posts(order: VOTES, first: %(limit)s) {
                edges {
                    node {
                        id
                        name
                        tagline
                        description
                        votesCount
                        url
                        commentsCount
                        topics { edges { node { name } } }
                        comments(first: 5) { edges { node { body } } }
                    }
                }
            }
        }
        """ % {"limit": limit}

        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.producthunt.com/v2/api/graphql",
                json={"query": query},
                headers=headers,
            )

            if resp.status_code != 200:
                logger.error(f"PH API returned {resp.status_code}: {resp.text[:200]}")
                return await self._scrape_public(limit)

            data = resp.json()
            edges = data.get("data", {}).get("posts", {}).get("edges", [])

            for edge in edges:
                node = edge["node"]
                comments = [
                    c["node"]["body"][:300]
                    for c in node.get("comments", {}).get("edges", [])
                    if c["node"].get("body")
                ]
                tags = [
                    t["node"]["name"]
                    for t in node.get("topics", {}).get("edges", [])
                ]

                trends.append(TrendData(
                    source="product_hunt",
                    title=node["name"],
                    description=node.get("tagline", ""),
                    url=node.get("url", f"https://producthunt.com/posts/{node['name'].lower().replace(' ', '-')}"),
                    upvotes=node.get("votesCount", 0),
                    comments=comments,
                    tags=tags,
                ))

        logger.info(f"Scraped {len(trends)} products from Product Hunt")
        return trends

    async def _scrape_public(self, limit: int) -> List[TrendData]:
        """Fallback: scrape Product Hunt via web."""
        import re
        from bs4 import BeautifulSoup

        trends = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get("https://www.producthunt.com/", headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            })
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Extract what we can from the page
                titles = soup.find_all("a", href=re.compile(r"/posts/"))
                for title_el in titles[:limit]:
                    text = title_el.get_text(strip=True)
                    if text and len(text) > 3:
                        trends.append(TrendData(
                            source="product_hunt",
                            title=text,
                            description="",
                            url=f"https://producthunt.com{title_el.get('href', '')}",
                            upvotes=0,
                            comments=[],
                            tags=[],
                        ))

        logger.info(f"Scraped {len(trends)} products from Product Hunt (public)")
        return trends

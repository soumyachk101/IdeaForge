"""Reddit scraper using PRAW."""
import logging
from typing import List

from scrapers.base import BaseScraper, TrendData
from config import CONFIG

logger = logging.getLogger("ideaforge.scrapers.reddit")

SUBREDDITS = ["SaaS", "microsaas", "entrepreneur", "startups", "indiehackers"]


class RedditScraper(BaseScraper):
    def __init__(self):
        import praw
        self.reddit = praw.Reddit(
            client_id=CONFIG["reddit_client_id"],
            client_secret=CONFIG["reddit_client_secret"],
            user_agent=CONFIG["reddit_user_agent"],
        )

    async def scrape(self, limit: int = 20) -> List[TrendData]:
        """Scrapes complaint/pain-point posts from SaaS-related subreddits."""
        trends = []
        per_sub = max(1, limit // len(SUBREDDITS))

        for sub_name in SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(sub_name)
                for post in subreddit.hot(limit=per_sub):
                    # Collect comments
                    comments = []
                    post.comments.replace_more(limit=0)
                    for comment in post.comments[:5]:
                        if comment.body and len(comment.body) > 20:
                            comments.append(comment.body[:300])

                    tags = [sub_name]
                    if post.link_flair_text:
                        tags.append(post.link_flair_text)

                    trends.append(TrendData(
                        source="reddit",
                        title=post.title,
                        description=post.selftext[:500] if post.selftext else "",
                        url=f"https://reddit.com{post.permalink}",
                        upvotes=post.score,
                        comments=comments,
                        tags=tags,
                    ))
            except Exception as e:
                logger.warning(f"Failed to scrape r/{sub_name}: {e}")

        logger.info(f"Scraped {len(trends)} posts from Reddit")
        return trends[:limit]

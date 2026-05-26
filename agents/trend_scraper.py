"""Trend Scraper Agent - discovers trending products and user complaints."""
from crewai import Agent

from tools.scraper_tools import (
    ScrapeHackerNewsTool,
    ScrapeRedditTool,
    ScrapeProductHuntTool,
    ScrapeIndieHackersTool,
)
from llm.ollama_client import get_crewai_llm
from llm.prompts import TREND_SCRAPER_PROMPT


def create_trend_scraper_agent() -> Agent:
    return Agent(
        role="Trend Scraper",
        goal="Discover the latest trending micro-SaaS products and extract user complaints, pain points, and emerging market opportunities",
        backstory=TREND_SCRAPER_PROMPT,
        tools=[
            ScrapeHackerNewsTool(),
            ScrapeRedditTool(),
            ScrapeProductHuntTool(),
            ScrapeIndieHackersTool(),
        ],
        llm=get_crewai_llm(),
        verbose=True,
        allow_delegation=False,
    )

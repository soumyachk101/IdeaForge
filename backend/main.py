"""IdeaForge CLI entrypoint."""
import sys
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    command = sys.argv[1] if len(sys.argv) > 1 else "serve"

    if command == "serve":
        from api.main import main as serve
        serve()
    elif command == "ingest":
        from rag.ingest import ingest_all
        ingest_all()
    elif command == "generate":
        niche = sys.argv[2] if len(sys.argv) > 2 else "developer tools"
        from agents.crew import run_idea_pipeline
        result = run_idea_pipeline(niche=niche)
        print(result)
    elif command == "scrape":
        import asyncio
        from scrapers.hacker_news import HackerNewsScraper
        trends = asyncio.run(HackerNewsScraper().scrape(5))
        for t in trends:
            print(f"[{t.upvotes}] {t.title} - {t.url}")
    else:
        print(f"Unknown command: {command}")
        print("Usage: python main.py [serve|ingest|generate|scrape]")
        sys.exit(1)


if __name__ == "__main__":
    main()

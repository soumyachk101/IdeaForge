# IdeaForge Backend

Python backend powering the multi-agent idea discovery pipeline.

## Architecture

```
backend/
├── config.py              ← Centralized config from .env
├── main.py                ← CLI entrypoint (serve|ingest|generate|scrape)
├── pyproject.toml         ← Dependencies (uv managed)
│
├── agents/                ← CrewAI agent definitions
│   ├── crew.py            ←   Sequential orchestration
│   ├── trend_scraper.py   ←   Agent 1: 4 scraper tools
│   ├── synthesizer.py     ←   Agent 2: RAG retriever tool
│   └── vc_agent.py        ←   Agent 3: pure reasoning
│
├── scrapers/              ← Data source scrapers
│   ├── base.py            ←   TrendData model + BaseScraper ABC
│   ├── hacker_news.py     ←   HN Firebase API (async)
│   ├── reddit.py          ←   PRAW (sync, reads CONFIG internally)
│   ├── product_hunt.py    ←   GraphQL API + HTML fallback
│   └── indie_hackers.py   ←   BeautifulSoup HTML scraping
│
├── rag/                   ← RAG pipeline
│   ├── embedder.py        ←   SentenceTransformers (MPS/CPU auto)
│   ├── chroma_client.py   ←   ChromaDB wrapper (4 collections)
│   ├── retriever.py       ←   Hybrid vector+BM25+RRF
│   ├── ingest.py          ←   Seed data ingestion
│   └── seed_data/         ←   Pre-built JSON knowledge base
│
├── llm/                   ← LLM layer
│   ├── ollama_client.py   ←   Ollama + Anthropic + CrewAI factory
│   └── prompts.py         ←   System prompts for all 3 agents
│
├── tools/                 ← CrewAI tools
│   ├── scraper_tools.py   ←   Scrapers wrapped as BaseTool
│   └── rag_tools.py       ←   RAG retriever as BaseTool (singleton)
│
└── api/                   ← FastAPI routes
    ├── main.py            ←   App setup + CORS + lifespan
    ├── models.py          ←   Pydantic request/response models
    └── routes/
        ├── health.py      ←   /api/health, /api/stats
        ├── ideas.py       ←   /api/ideas/generate (SSE), /api/ideas
        ├── trends.py      ←   /api/trends, /api/trends/scrape
        └── rag.py         ←   /api/rag/query, /ingest, /browse
```

## Setup

```bash
# Install dependencies
uv sync

# Copy and edit environment file
cp .env.example .env

# Seed RAG database
uv run python -m rag.ingest

# Start server
uv run uvicorn api.main:app --reload --port 8000
```

## CLI

```bash
uv run python main.py serve              # Start API server
uv run python main.py ingest             # Seed RAG database
uv run python main.py generate "legal"   # Generate ideas from CLI
uv run python main.py scrape             # Test HN scraper
```

## Key Design Decisions

- **Scrapers read CONFIG internally** — don't pass credentials as constructor args
- **rag_tools uses lazy singletons** — TextEmbedder loads once, reused across calls
- **scraper_tools uses _run_async()** — safe inside existing event loops
- **All imports are relative to backend/** — run from this directory

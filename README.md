 ```
  ___                   _____                    
 |_  |                 |  ___|                   
   | | __ _  __ _  __ _| |__ _ __ __ _  ___ ___  
   | |/ _` |/ _` |/ _` |  __| '__/ _` |/ __/ _ \ 
   | | (_| | (_| | (_| | |__| | | (_| | (_|  __/ 
   \_/\__,_|\__, |\__,_\____/_|  \__,_|\___\___| 
              __/ |                               
             |___/                                
```

<p align="center">
  <strong>Multi-Agent Micro-SaaS Idea Discovery Engine</strong><br>
  <em>Scrape trends. Match with data. Generate business proposals.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Next.js-14-000000?style=flat&logo=next.js&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/CrewAI-0.28+-FF6B35?style=flat" alt="CrewAI">
  <img src="https://img.shields.io/badge/ChromaDB-0.5+-8B5CF6?style=flat" alt="ChromaDB">
  <img src="https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="MIT License">
</p>

---

## What is IdeaForge?

IdeaForge is an **AI-powered system** that discovers monetizable micro-SaaS ideas by:

1. **Scraping** real-time trends from Product Hunt, Hacker News, Reddit, and Indie Hackers
2. **Matching** those trends against a knowledge base of proven monetization frameworks
3. **Generating** actionable business proposals with exact tech stacks and pricing

Think of it as having 3 AI analysts working for you 24/7 — one watches the market, one cross-references the data, and one writes the business plan.

---

## How It Works

```
                        IDEA FORGE PIPELINE
                        ===================

  ┌─────────────────────────────────────────────────────────────────┐
  │                     3 AI AGENTS (CrewAI)                        │
  │                                                                 │
  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
  │   │  🕵️ TREND    │───▶│  🧠 SYNTH    │───▶│  💰 VC       │     │
  │   │  SCRAPER     │    │  ESIZER      │    │  ADVISOR     │     │
  │   │              │    │              │    │              │     │
  │   │ Scrapes 4    │    │ Searches RAG │    │ Creates      │     │
  │   │ sources for  │    │ for matching │    │ actionable   │     │
  │   │ trends &     │    │ frameworks & │    │ proposals    │     │
  │   │ pain points  │    │ gaps         │    │ with pricing │     │
  │   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
  │          │                   │                   │             │
  └──────────┼───────────────────┼───────────────────┼─────────────┘
             │                   │                   │
             ▼                   ▼                   ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │ DATA SOURCES │    │ KNOWLEDGE    │    │   OUTPUT     │
  │              │    │ BASE (RAG)   │    │              │
  │ • Product    │    │              │    │ • Product    │
  │   Hunt       │    │ • 7 Monetiz- │    │   Name       │
  │ • Hacker     │    │   ation      │    │ • Tech Stack │
  │   News       │    │   Frameworks │    │ • Pricing    │
  │ • Reddit     │    │ • 20 Pain    │    │ • GTM        │
  │   (5 subs)   │    │   Points     │    │   Strategy   │
  │ • Indie      │    │ • 12 Case    │    │ • Revenue    │
  │   Hackers    │    │   Studies    │    │   Projection │
  └──────────────┘    └──────────────┘    └──────────────┘
```

### Step-by-Step Flow

```
USER selects niche
        │
        ▼
┌─────────────────────────────┐
│ Agent 1: TREND SCRAPER      │
│                             │
│ Scrapes:                    │
│  • Product Hunt (GraphQL)   │
│  • Hacker News (Firebase)   │
│  • Reddit (PRAW)            │
│  • Indie Hackers (HTML)     │
│                             │
│ Output: Trend report with   │
│ pain points & market gaps   │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Agent 2: SYNTHESIZER        │
│                             │
│ Searches RAG database for:  │
│  • Matching monetization    │
│    frameworks               │
│  • Similar pain points      │
│  • Startup case studies     │
│                             │
│ Output: Ranked opportunities│
│ with scoring                │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Agent 3: VC ADVISOR         │
│                             │
│ Creates proposals with:     │
│  • Product name & one-liner │
│  • Exact tech stack         │
│  • Pricing ($10-$50/mo)     │
│  • GTM strategy             │
│  • Revenue projections      │
│                             │
│ Output: 3-5 actionable      │
│ micro-SaaS proposals        │
└─────────────────────────────┘
```

---

## Architecture

```
IDEAFORGE ARCHITECTURE
======================

┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                           │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Generate │  │  Ideas   │  │  Trends  │  │ Knowledge Base   │   │
│  │  Page    │  │ Gallery  │  │ Browser  │  │ (Search/Browse)  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬─────────┘   │
│       │              │             │                  │             │
│       └──────────────┼─────────────┼──────────────────┘             │
│                      │                                             │
│              ┌───────▼────────┐                                    │
│              │   API Client   │                                    │
│              │   (lib/api.ts) │                                    │
│              └───────┬────────┘                                    │
│                      │                                             │
│              ┌───────▼────────┐                                    │
│              │  Next.js Proxy │                                    │
│              │ /api/* → :8000 │                                    │
│              └───────┬────────┘                                    │
└──────────────────────┼──────────────────────────────────────────────┘
                       │
                       │ HTTP + SSE
                       │
┌──────────────────────┼──────────────────────────────────────────────┐
│                      │      BACKEND (FastAPI + CrewAI)              │
│              ┌───────▼────────┐                                     │
│              │   FastAPI App  │                                     │
│              │   (api/main)   │                                     │
│              └───────┬────────┘                                     │
│                      │                                             │
│    ┌─────────────────┼──────────────────┐                          │
│    │                 │                  │                          │
│    ▼                 ▼                  ▼                          │
│ ┌────────┐    ┌────────────┐    ┌─────────────┐                   │
│ │ Ideas  │    │  Trends    │    │    RAG      │                   │
│ │ Route  │    │  Route     │    │   Route     │                   │
│ └───┬────┘    └─────┬──────┘    └──────┬──────┘                   │
│     │               │                  │                          │
│     ▼               ▼                  ▼                          │
│ ┌──────────────────────────────────────────────────────────────┐  │
│ │                   CREWAI ORCHESTRATION                       │  │
│ │                                                              │  │
│ │  ┌──────────┐  ┌──────────────┐  ┌─────────────────────┐   │  │
│ │  │ Trend    │  │ Synthesizer  │  │  VC/Monetization    │   │  │
│ │  │ Scraper  │  │ Agent        │  │  Advisor            │   │  │
│ │  │ Agent    │  │              │  │                     │   │  │
│ │  └────┬─────┘  └──────┬───────┘  └──────────┬──────────┘   │  │
│ │       │               │                      │              │  │
│ │       ▼               ▼                      ▼              │  │
│ │  ┌──────────┐  ┌──────────────┐  ┌─────────────────────┐   │  │
│ │  │ Scraper  │  │ RAG Retriever│  │  System Prompts     │   │  │
│ │  │ Tools    │  │ Tool         │  │                     │   │  │
│ │  └────┬─────┘  └──────┬───────┘  └─────────────────────┘   │  │
│ └───────┼───────────────┼─────────────────────────────────────┘  │
│         │               │                                        │
│         ▼               ▼                                        │
│  ┌────────────┐  ┌──────────────┐                                │
│  │ SCRAPERS   │  │  RAG PIPELINE│                                │
│  │            │  │              │                                │
│  │ • HN API   │  │ • ChromaDB   │                                │
│  │ • Reddit   │  │ • BM25       │                                │
│  │ • PH API   │  │ • Embeddings │                                │
│  │ • IH HTML  │  │ • RRF Fusion │                                │
│  └────────────┘  └──────────────┘                                │
└───────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
IdeaForge/
│
├── backend/                          # Python backend
│   ├── pyproject.toml                # Dependencies & project config
│   ├── .env.example                  # Environment variables template
│   ├── .python-version               # Python 3.12
│   ├── config.py                     # Centralized configuration
│   ├── main.py                       # CLI: serve | ingest | generate | scrape
│   │
│   ├── agents/                       # CrewAI 3-agent pipeline
│   │   ├── crew.py                   #   └─ Orchestrates sequential flow
│   │   ├── trend_scraper.py          #   └─ Agent 1: scrapes 4 sources
│   │   ├── synthesizer.py            #   └─ Agent 2: RAG gap analysis
│   │   └── vc_agent.py               #   └─ Agent 3: business proposals
│   │
│   ├── scrapers/                     # Data source scrapers
│   │   ├── base.py                   #   └─ TrendData model + BaseScraper
│   │   ├── hacker_news.py            #   └─ HN Firebase API
│   │   ├── reddit.py                 #   └─ PRAW (5 subreddits)
│   │   ├── product_hunt.py           #   └─ GraphQL API + fallback
│   │   └── indie_hackers.py          #   └─ BeautifulSoup scraping
│   │
│   ├── rag/                          # RAG pipeline
│   │   ├── embedder.py               #   └─ SentenceTransformers (MPS/CPU)
│   │   ├── chroma_client.py          #   └─ ChromaDB (4 collections)
│   │   ├── retriever.py              #   └─ Hybrid vector+BM25+RRF
│   │   ├── ingest.py                 #   └─ Seed data ingestion
│   │   └── seed_data/                #   └─ Pre-built knowledge base
│   │       ├── monetization_frameworks.json
│   │       ├── pain_points.json
│   │       └── startup_case_studies.json
│   │
│   ├── llm/                          # LLM layer
│   │   ├── ollama_client.py          #   └─ Ollama + Anthropic + CrewAI
│   │   └── prompts.py                #   └─ System prompts for agents
│   │
│   ├── tools/                        # CrewAI tools
│   │   ├── scraper_tools.py          #   └─ Scrapers as BaseTool
│   │   └── rag_tools.py              #   └─ RAG as BaseTool
│   │
│   └── api/                          # FastAPI backend
│       ├── main.py                   #   └─ App + CORS + lifespan
│       ├── models.py                 #   └─ Pydantic models
│       └── routes/
│           ├── health.py             #   └─ /api/health, /api/stats
│           ├── ideas.py              #   └─ /api/ideas/generate (SSE)
│           ├── trends.py             #   └─ /api/trends/scrape
│           └── rag.py                #   └─ /api/rag/query, /browse
│
└── frontend/                         # Next.js 14 dashboard
    ├── next.config.ts                # API proxy to :8000
    ├── lib/api.ts                    # API client
    └── app/
        ├── layout.tsx                # Navigation + layout
        ├── page.tsx                  # Generate (SSE streaming)
        ├── ideas/
        │   ├── page.tsx              # Ideas gallery
        │   └── [id]/page.tsx         # Idea detail
        ├── trends/page.tsx           # Trend browser
        └── knowledge/page.tsx        # RAG search + browse
```

---

## Quick Start

### Prerequisites

- **Python 3.11+** — `python3 --version`
- **Node.js 18+** — `node --version`
- **uv** (Python package manager) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Ollama** (for local LLM) — [ollama.ai](https://ollama.ai)

### 1. Install Backend

```bash
cd IdeaForge/backend

# Copy environment file
cp .env.example .env

# Edit .env with your API keys (optional - scrapers work without keys)
# RECOMMENDED: Get Reddit API credentials for full access
# OPTIONAL: Get Product Hunt API token

# Install Python dependencies
uv sync
```

### 2. Seed the Knowledge Base

```bash
# Ingest monetization frameworks, pain points, and case studies
uv run python -m rag.ingest
```

```
Ingesting seed data...
  monetization_frameworks: 7 documents, 7 chunks
  pain_points: 12 documents, 12 chunks
  startup_case_studies: 7 documents, 7 chunks
Done! Total: 26 documents in 3 collections
```

### 3. Start the Backend

```bash
# Start FastAPI server
uv run uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

```
INFO:     IdeaForge API starting...
INFO:       LLM provider: ollama
INFO:       ChromaDB path: .ideaforge_data/chroma
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     API docs at http://127.0.0.1:8000/docs
```

### 4. Start Ollama (in another terminal)

```bash
# Pull a model and start serving
ollama pull deepseek-coder-v2
ollama serve
```

### 5. Start the Frontend

```bash
# In another terminal
cd IdeaForge/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

```
  ▲ Next.js 16.2.6
  - Local:    http://localhost:3000
  - Network:  http://192.168.x.x:3000
```

### 6. Open & Generate

Open **http://localhost:3000** in your browser.

1. Select a niche (e.g., "Developer Tools")
2. Click **Generate Ideas**
3. Watch the 3 agents work in real-time via SSE streaming

---

## API Endpoints

```
┌──────────┬──────────────────────────┬──────────────────────────────────┐
│  Method  │  Endpoint                │  Description                     │
├──────────┼──────────────────────────┼──────────────────────────────────┤
│  GET     │  /api/health             │  Health check + ChromaDB status  │
│  GET     │  /api/stats              │  Document counts per collection  │
│          │                          │                                  │
│  POST    │  /api/ideas/generate     │  Generate ideas (SSE stream)     │
│  GET     │  /api/ideas              │  List all generated ideas        │
│  GET     │  /api/ideas/{id}         │  Get idea by ID                  │
│          │                          │                                  │
│  GET     │  /api/trends             │  Get cached trends               │
│  POST    │  /api/trends/scrape      │  Scrape fresh trends             │
│          │                          │                                  │
│  POST    │  /api/rag/query          │  Search RAG knowledge base       │
│  POST    │  /api/rag/ingest/seed    │  Ingest seed data                │
│  GET     │  /api/rag/browse/{col}   │  Browse collection documents     │
│          │                          │                                  │
│  GET     │  /docs                   │  Swagger UI (auto-generated)     │
└──────────┴──────────────────────────┴──────────────────────────────────┘
```

### Generate Ideas (SSE Stream)

```bash
curl -N -X POST http://127.0.0.1:8000/api/ideas/generate \
  -H "Content-Type: application/json" \
  -d '{"niche": "developer tools"}'
```

```
data: {"type":"start","niche":"developer tools","id":"a1b2c3d4e5f6"}
data: {"type":"result","id":"a1b2c3d4e5f6","content":"## LogLens AI\n\n### The Problem\n..."}
data: {"type":"done","id":"a1b2c3d4e5f6"}
```

### Search RAG

```bash
curl -X POST http://127.0.0.1:8000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "developer tools for log analysis", "collection": "all"}'
```

---

## Knowledge Base (RAG)

The RAG pipeline uses **hybrid retrieval** — combining vector search with BM25 keyword search, fused via Reciprocal Rank Fusion.

```
                    HYBRID RETRIEVAL
                    ================

    Query: "developer tools for log analysis"
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  ┌──────────┐           ┌──────────┐
  │  VECTOR  │           │   BM25   │
  │  SEARCH  │           │  SEARCH  │
  │          │           │          │
  │  ChromaDB│           │  TF-IDF  │
  │  cosine  │           │  keyword │
  │  similarity           │  matching│
  └─────┬────┘           └─────┬────┘
        │                      │
        └──────────┬───────────┘
                   ▼
          ┌────────────────┐
          │  RECIPROCAL    │
          │  RANK FUSION   │
          │                │
          │  score =       │
          │  Σ 1/(k+rank)  │
          └────────┬───────┘
                   │
                   ▼
           Ranked Results
```

### Seed Data Contents

| Collection               | Documents | Description                                    |
|--------------------------|-----------|------------------------------------------------|
| `monetization_frameworks`| 7         | Freemium, API-as-a-service, Subscription, etc. |
| `pain_points`            | 12        | "I wish there was a tool that..." complaints   |
| `startup_case_studies`   | 7         | Real micro-SaaS with revenue & tech stacks     |

### Adding Custom Data

```bash
# Via API
curl -X POST http://127.0.0.1:8000/api/rag/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "collection": "pain_points",
    "documents": [
      {
        "title": "My Custom Pain Point",
        "content": "As a developer, I spend 2 hours every day...",
        "category": "developer_tools",
        "source": "manual"
      }
    ]
  }'

# Then rebuild BM25 index by restarting the server
```

---

## LLM Configuration

IdeaForge supports **two LLM providers**, switchable via environment variable:

```
┌─────────────────────────────────────────────────────────────────┐
│                     LLM CONFIGURATION                           │
│                                                                 │
│  .env file:                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ # Local (default)                                         │  │
│  │ LLM_PROVIDER=ollama                                       │  │
│  │ OLLAMA_BASE_URL=http://localhost:11434                     │  │
│  │ OLLAMA_MODEL=deepseek-coder-v2                            │  │
│  │                                                           │  │
│  │ # Production (switch to Anthropic)                        │  │
│  │ # LLM_PROVIDER=anthropic                                  │  │
│  │ # ANTHROPIC_API_KEY=sk-ant-...                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Flow:                                                          │
│  ┌──────────────┐     ┌───────────────┐     ┌───────────────┐  │
│  │ config.py    │────▶│ ollama_client │────▶│ CrewAI Agent  │  │
│  │ reads .env   │     │ get_crewai_   │     │ .llm = LLM()  │  │
│  │              │     │ llm()         │     │               │  │
│  └──────────────┘     └───────────────┘     └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Recommended Models

| Provider   | Model                | Use Case                     |
|------------|---------------------|------------------------------|
| Ollama     | `deepseek-coder-v2` | Best for local dev (coding)  |
| Ollama     | `llama3`            | Good general purpose         |
| Ollama     | `mistral`           | Fast, decent quality         |
| Anthropic  | `claude-sonnet-4`   | Production quality           |

---

## Frontend Pages

```
┌─────────────────────────────────────────────────────────────────┐
│                         NAVIGATION                              │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Generate │  │  Ideas   │  │  Trends  │  │ Knowledge    │   │
│  │    /     │  │ /ideas   │  │ /trends  │  │ /knowledge   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘

GENERATE PAGE (/)
├── Niche selector (pill buttons)
├── "Generate Ideas" button
├── SSE progress stream
│   ├── Agent 1: Trend Scraper ── running
│   ├── Agent 2: Synthesizer ─── running
│   └── Agent 3: VC Advisor ──── running
└── Generated proposals output

IDEAS PAGE (/ideas)
├── Idea cards grid
│   ├── Niche badge
│   ├── Preview text
│   └── Created date
└── Click to expand full proposal

TRENDS PAGE (/trends)
├── Source filter buttons
├── "Scrape Now" button
└── Trend cards
    ├── Source badge (HN/Reddit/PH/IH)
    ├── Title + upvotes
    ├── Description preview
    └── Tags

KNOWLEDGE PAGE (/knowledge)
├── Seed data ingestion controls
├── Search bar + collection filter
└── Results
    ├── Score (cosine distance)
    ├── Document text
    └── Metadata (title, category)
```

---

## Environment Variables

```bash
# ============================================
# IDEA FORGE ENVIRONMENT VARIABLES
# ============================================
# Copy this file: cp .env.example .env

# --- LLM Configuration ---
LLM_PROVIDER=ollama                  # "ollama" or "anthropic"
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-coder-v2
ANTHROPIC_API_KEY=                   # Only needed if LLM_PROVIDER=anthropic

# --- Reddit API (recommended) ---
# Get from: https://www.reddit.com/prefs/apps
# 1. Create an app (type: "script")
# 2. Copy client ID and secret
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=IdeaForge/0.1.0

# --- Product Hunt API (optional) ---
# Get from: https://www.producthunt.com/v2/oauth/applications
# Without token, falls back to HTML scraping (less reliable)
PRODUCT_HUNT_TOKEN=

# --- RAG Configuration ---
CHROMA_PATH=.ideaforge_data/chroma   # Where ChromaDB stores data
EMBEDDING_MODEL=all-MiniLM-L6-v2     # Sentence-transformers model

# --- Server ---
API_HOST=127.0.0.1
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'agents'"

```bash
# You're running from the wrong directory.
# Always run Python commands from the backend/ directory:
cd IdeaForge/backend
uv run python -m rag.ingest
```

### "Ollama connection refused"

```bash
# Start Ollama first:
ollama serve

# In another terminal, pull a model:
ollama pull deepseek-coder-v2
```

### "No results from Reddit scraper"

```bash
# Reddit requires API credentials.
# 1. Go to https://www.reddit.com/prefs/apps
# 2. Create a "script" app
# 3. Add credentials to .env:
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
```

### "TextEmbedder takes 30+ seconds to load"

```bash
# First load downloads the model (~80MB).
# Subsequent loads use cache and are fast.
# If on Apple Silicon, MPS acceleration is auto-detected.
```

### "ChromaDB collection not found"

```bash
# Re-ingest seed data:
cd IdeaForge/backend
uv run python -m rag.ingest --reset
```

### Frontend shows "Failed to fetch"

```bash
# Make sure the backend is running on port 8000:
curl http://127.0.0.1:8000/api/health

# If not, start it:
cd IdeaForge/backend
uv run uvicorn api.main:app --reload
```

---

## CLI Commands

```bash
cd IdeaForge/backend

# Start the API server
uv run python main.py serve

# Ingest seed data into RAG
uv run python main.py ingest

# Generate ideas directly (no frontend)
uv run python main.py generate "developer tools"

# Quick test: scrape Hacker News
uv run python main.py scrape
```

---

## Tech Stack Deep Dive

```
┌─────────────────────────────────────────────────────────────────┐
│                        TECH STACK                               │
│                                                                 │
│  FRONTEND                                                       │
│  ├── Next.js 14 (App Router)     ── React framework             │
│  ├── TypeScript                  ── Type safety                 │
│  ├── Tailwind CSS                ── Utility-first styling       │
│  ├── SSE (fetch + ReadableStream)── Real-time streaming         │
│  └── next.config.ts rewrites     ── API proxy                   │
│                                                                 │
│  BACKEND                                                        │
│  ├── FastAPI                     ── Async web framework         │
│  ├── CrewAI                      ── Multi-agent orchestration   │
│  ├── Pydantic                    ── Data validation             │
│  ├── uvicorn                     ── ASGI server                 │
│  └── sse-starlette               ── Server-Sent Events          │
│                                                                 │
│  AI / ML                                                        │
│  ├── Ollama                      ── Local LLM serving           │
│  ├── SentenceTransformers        ── Text embeddings             │
│  │   └── all-MiniLM-L6-v2        ── 384-dim, MPS-accelerated    │
│  ├── ChromaDB                    ── Vector database              │
│  ├── rank-bm25                   ── BM25 keyword search         │
│  └── Reciprocal Rank Fusion      ── Hybrid search merging       │
│                                                                 │
│  SCRAPERS                                                       │
│  ├── httpx                       ── Async HTTP client           │
│  ├── PRAW                        ── Reddit API wrapper          │
│  ├── BeautifulSoup4              ── HTML parsing                │
│  └── Product Hunt GraphQL API    ── Product data                │
│                                                                 │
│  PACKAGE MANAGEMENT                                             │
│  ├── uv                          ── Python (fast, deterministic)│
│  └── npm                         ── Node.js                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `cd backend && uv run python -c "from api.main import app; print('OK')"`
5. Submit a pull request

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built with CrewAI, FastAPI, ChromaDB, and Next.js</strong><br>
  <em>Discover your next micro-SaaS idea in minutes, not months.</em>
</p>

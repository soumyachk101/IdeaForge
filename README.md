<h1 align="center">
<pre>
 ___                   _____                    
|_  |                 |  ___|                   
  | | __ _  __ _  __ _| |__ _ __ __ _  ___ ___  
  | |/ _` |/ _` |/ _` |  __| '__/ _` |/ __/ _ \ 
  | | (_| | (_| | (_| | |__| | | (_| | (_|  __/ 
  \_/\__,_|\__, |\__,_\____/_|  \__,_|\___\___| 
             __/ |                               
            |___/                                
</pre>
</h1>

<p align="center">
  <strong>Multi-Agent Micro-SaaS Idea Discovery Engine</strong><br>
  <em>Scrape trends. Match with data. Generate business proposals.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/CrewAI-0.28+-FF6B35?style=for-the-badge" alt="CrewAI">
  <img src="https://img.shields.io/badge/ChromaDB-0.5+-8B5CF6?style=for-the-badge" alt="ChromaDB">
  <img src="https://img.shields.io/badge/FastAPI-0.111+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> &bull;
  <a href="#-how-it-works">How It Works</a> &bull;
  <a href="#-architecture">Architecture</a> &bull;
  <a href="#-api">API</a> &bull;
  <a href="#-troubleshooting">Troubleshooting</a>
</p>

---

## What is IdeaForge?

IdeaForge is an **AI-powered multi-agent system** that discovers monetizable micro-SaaS ideas by combining real-time trend scraping, RAG-based knowledge matching, and autonomous business proposal generation.

> **3 AI agents working 24/7** — one watches the market, one cross-references the data, and one writes the business plan.

<p align="center">
  <img src="https://img.shields.io/badge/Real--time_Trend_Scraping-4_sources-blueviolet?style=flat-square" alt="Trend Scraping">
  <img src="https://img.shields.io/badge/RAG_Knowledge_Matching-Hybrid_Search-orange?style=flat-square" alt="RAG Matching">
  <img src="https://img.shields.io/badge/Business_Proposals-Actionable_Outputs-green?style=flat-square" alt="Proposals">
</p>

---

## How It Works

```mermaid
flowchart LR
    subgraph INPUT["User Input"]
        A["Niche Selection"]
    end

    subgraph AGENTS["CrewAI Multi-Agent Pipeline"]
        B["Trend Scraper - Scrapes 4 sources"]
        C["Synthesizer - RAG gap analysis"]
        D["VC Advisor - Business proposals"]
    end

    subgraph SOURCES["Data Sources"]
        E["Product Hunt - GraphQL API"]
        F["Hacker News - Firebase API"]
        G["Reddit - PRAW + 5 subs"]
        H["Indie Hackers - HTML Scraping"]
    end

    subgraph RAG["Knowledge Base"]
        I[("ChromaDB Vector Store")]
        J["BM25 Keyword Search"]
        K["7 Monetization Frameworks"]
        L["20 Pain Points"]
        M["12 Case Studies"]
    end

    subgraph OUTPUT["Output"]
        N["3-5 Actionable Micro-SaaS Proposals"]
    end

    A --> B
    B --> C --> D
    E --> B
    F --> B
    G --> B
    H --> B
    I --> C
    J --> C
    K --> C
    L --> C
    M --> C
    D --> N

    style A fill:#4CAF50,stroke:#388E3C,color:#fff
    style B fill:#2196F3,stroke:#1565C0,color:#fff
    style C fill:#FF9800,stroke:#E65100,color:#fff
    style D fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style N fill:#4CAF50,stroke:#388E3C,color:#fff
```

### Pipeline Flow

```mermaid
sequenceDiagram
    participant U as User
    participant A1 as Trend Scraper
    participant A2 as Synthesizer
    participant A3 as VC Advisor
    participant DB as ChromaDB

    U->>A1: Select niche
    activate A1
    A1->>A1: Scrape Product Hunt
    A1->>A1: Scrape Hacker News
    A1->>A1: Scrape Reddit (5 subs)
    A1->>A1: Scrape Indie Hackers
    A1-->>A2: Trend report + pain points
    deactivate A1

    activate A2
    A2->>DB: Vector search (cosine similarity)
    A2->>DB: BM25 keyword search
    DB-->>A2: Matching frameworks + case studies
    A2->>A2: Reciprocal Rank Fusion
    A2-->>A3: Ranked opportunities
    deactivate A2

    activate A3
    A3->>A3: Generate product name
    A3->>A3: Select tech stack
    A3->>A3: Define pricing ($10-$50/mo)
    A3->>A3: Create GTM strategy
    A3-->>U: 3-5 actionable proposals (SSE stream)
    deactivate A3
```

---

## Architecture

### Full System Workflow

```mermaid
graph TB
    subgraph FRONTEND["Frontend - Next.js 14"]
        P1["Generate Page"]
        P2["Ideas Gallery"]
        P3["Trends Browser"]
        P4["Knowledge Search"]
        P1 --> API["API Client - lib/api.ts"]
        P2 --> API
        P3 --> API
        P4 --> API
        API --> PROXY["Next.js Proxy /api/* to :8000"]
    end

    subgraph BACKEND["Backend - FastAPI"]
        PROXY -->|HTTP + SSE| FAST["FastAPI App"]
        FAST --> R1["Ideas Route"]
        FAST --> R2["Trends Route"]
        FAST --> R3["RAG Route"]
    end

    subgraph CREW["CrewAI Orchestration"]
        R1 --> A1["Trend Scraper Agent"]
        R1 --> A2["Synthesizer Agent"]
        R1 --> A3["VC Advisor Agent"]
        A1 -->|trends + pain points| A2
        A2 -->|ranked opportunities| A3
    end

    subgraph TOOLS["Agent Tools"]
        A1 --> T1["Scraper Tools"]
        A2 --> T2["RAG Retriever Tool"]
        A3 --> T3["System Prompts"]
    end

    subgraph SCRAPERS["Scrapers"]
        T1 --> S1["HN Firebase API"]
        T1 --> S2["Reddit PRAW"]
        T1 --> S3["Product Hunt GraphQL"]
        T1 --> S4["Indie Hackers HTML"]
    end

    subgraph RAG["RAG Pipeline"]
        T2 --> DB[("ChromaDB - 4 collections")]
        T2 --> BM["BM25 Index"]
        T2 --> EM["Embeddings - all-MiniLM-L6-v2"]
    end

    subgraph LLM["LLM Providers"]
        A3 --> L1["Ollama - Local"]
        A3 --> L2["Anthropic - Cloud"]
    end

    subgraph DATASTORE["Data Store"]
        R2 --> SC["Scraped Trends Cache"]
        R3 --> RAG
    end

    A3 -->|SSE stream| OUT["Business Proposals"]
    OUT --> PROXY

    style FRONTEND fill:#e3f2fd,stroke:#1565C0
    style BACKEND fill:#fff3e0,stroke:#E65100
    style CREW fill:#fce4ec,stroke:#c62828
    style TOOLS fill:#f3e5f5,stroke:#6A1B9A
    style SCRAPERS fill:#e8f5e9,stroke:#2E7D32
    style RAG fill:#fff8e1,stroke:#f57f17
    style LLM fill:#e0f7fa,stroke:#00695c
    style DATASTORE fill:#efebe9,stroke:#4e342e
```

### Request Flow Sequence

```mermaid
sequenceDiagram
    participant U as User Browser
    participant NX as Next.js Proxy
    participant API as FastAPI
    participant CW as CrewAI
    participant S1 as Trend Scraper
    participant S2 as Synthesizer
    participant S3 as VC Advisor
    participant DB as ChromaDB
    participant LLM as Ollama / Anthropic

    U->>NX: POST /api/ideas/generate
    NX->>API: Forward request
    API->>CW: Kickoff CrewAI pipeline
    API-->>U: SSE stream opened

    activate CW
    CW->>S1: Task 1: Scrape trends
    S1->>S1: Scrape HN, Reddit, PH, IH
    S1-->>S2: Trend report + pain points

    CW->>S2: Task 2: Analyze with RAG
    S2->>DB: Vector + BM25 search
    DB-->>S2: Frameworks + case studies
    S2-->>S3: Ranked opportunities

    CW->>S3: Task 3: Generate proposals
    S3->>LLM: Generate business plan
    LLM-->>S3: Proposal content
    S3-->>API: Final output
    deactivate CW

    API-->>U: SSE: type=result
    API-->>U: SSE: type=done
```

### Data Layer Detail

```mermaid
graph LR
    subgraph SOURCES["External Sources"]
        PH["Product Hunt API"]
        HN["Hacker News API"]
        RD["Reddit PRAW"]
        IH["Indie Hackers"]
    end

    subgraph INGEST["Ingestion"]
        SC["Scraper Tools"]
        SD["Seed Data JSON"]
    end

    subgraph STORE["Storage"]
        CH[("ChromaDB")]
        BM["BM25 Index"]
        EM["Embeddings"]
    end

    subgraph QUERY["Query"]
        VR["Vector Retriever"]
        BR["BM25 Retriever"]
        RRF["Reciprocal Rank Fusion"]
    end

    subgraph OUTPUT["Output"]
        FR["Frameworks"]
        PP["Pain Points"]
        CS["Case Studies"]
    end

    PH --> SC
    HN --> SC
    RD --> SC
    IH --> SC
    SC --> CH
    SD --> CH
    CH --> EM
    CH --> VR
    BM --> BR
    VR --> RRF
    BR --> RRF
    RRF --> FR
    RRF --> PP
    RRF --> CS

    style SOURCES fill:#e8f5e9,stroke:#2E7D32
    style STORE fill:#fff8e1,stroke:#f57f17
    style QUERY fill:#f3e5f5,stroke:#6A1B9A
    style OUTPUT fill:#e3f2fd,stroke:#1565C0
```

---

## Tech Stack

```mermaid
flowchart TB
    CORE(("IdeaForge"))

    CORE --- FRONT["Frontend"]
    FRONT --- NEXT["Next.js 14"]
    FRONT --- TS["TypeScript"]
    FRONT --- TW["Tailwind CSS"]
    FRONT --- SSE["SSE Streaming"]

    CORE --- BACK["Backend"]
    BACK --- FAST["FastAPI"]
    BACK --- CREW["CrewAI"]
    BACK --- PYD["Pydantic"]
    BACK --- UVI["uvicorn"]

    CORE --- AIML["AI / ML"]
    AIML --- OLL["Ollama"]
    AIML --- CLAUDE["Anthropic Claude"]
    AIML --- ST["SentenceTransformers"]
    AIML --- CHROMA["ChromaDB"]
    AIML --- HYBRID["BM25 + RRF"]

    CORE --- SCRAPE["Scrapers"]
    SCRAPE --- PH["Product Hunt GraphQL"]
    SCRAPE --- HN["Hacker News API"]
    SCRAPE --- REDDIT["Reddit PRAW"]
    SCRAPE --- IH["Indie Hackers HTML"]

    CORE --- PKG["Package Mgmt"]
    PKG --- UV["uv"]
    PKG --- PY["Python"]
    PKG --- NPM["npm"]
    PKG --- NODE["Node.js"]

    style CORE fill:#858b88,stroke:#858b88,color:#111

    style FRONT fill:#090000,stroke:#090000,color:#f3f4f6
    style NEXT fill:#090000,stroke:#090000,color:#f3f4f6
    style TS fill:#090000,stroke:#090000,color:#f3f4f6
    style TW fill:#090000,stroke:#090000,color:#f3f4f6
    style SSE fill:#090000,stroke:#090000,color:#f3f4f6

    style BACK fill:#5f0f3f,stroke:#5f0f3f,color:#f3f4f6
    style FAST fill:#5f0f3f,stroke:#5f0f3f,color:#f3f4f6
    style CREW fill:#5f0f3f,stroke:#5f0f3f,color:#f3f4f6
    style PYD fill:#5f0f3f,stroke:#5f0f3f,color:#f3f4f6
    style UVI fill:#5f0f3f,stroke:#5f0f3f,color:#f3f4f6

    style AIML fill:#455d63,stroke:#455d63,color:#f3f4f6
    style OLL fill:#455d63,stroke:#455d63,color:#f3f4f6
    style CLAUDE fill:#455d63,stroke:#455d63,color:#f3f4f6
    style ST fill:#455d63,stroke:#455d63,color:#f3f4f6
    style CHROMA fill:#455d63,stroke:#455d63,color:#f3f4f6
    style HYBRID fill:#455d63,stroke:#455d63,color:#f3f4f6

    style SCRAPE fill:#5a351d,stroke:#5a351d,color:#f3f4f6
    style PH fill:#5a351d,stroke:#5a351d,color:#f3f4f6
    style HN fill:#5a351d,stroke:#5a351d,color:#f3f4f6
    style REDDIT fill:#5a351d,stroke:#5a351d,color:#f3f4f6
    style IH fill:#5a351d,stroke:#5a351d,color:#f3f4f6

    style PKG fill:#8b0e0e,stroke:#8b0e0e,color:#f3f4f6
    style UV fill:#8b0e0e,stroke:#8b0e0e,color:#f3f4f6
    style PY fill:#8b0e0e,stroke:#8b0e0e,color:#f3f4f6
    style NPM fill:#8b0e0e,stroke:#8b0e0e,color:#f3f4f6
    style NODE fill:#8b0e0e,stroke:#8b0e0e,color:#f3f4f6

    linkStyle 0,1,2,3,4 stroke:#120202,stroke-width:5px
    linkStyle 5,6,7,8,9 stroke:#6d1048,stroke-width:5px
    linkStyle 10,11,12,13,14,15 stroke:#4e686f,stroke-width:5px
    linkStyle 16,17,18,19,20 stroke:#6d401f,stroke-width:5px
    linkStyle 21,22,23,24,25 stroke:#930f0f,stroke-width:5px
```

---

## Quick Start

### Prerequisites

| Requirement | Check | Install |
|-------------|-------|---------|
| Python 3.11+ | `python3 --version` | [python.org](https://python.org) |
| Node.js 18+ | `node --version` | [nodejs.org](https://nodejs.org) |
| uv | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Ollama | `ollama --version` | [ollama.ai](https://ollama.ai) |

### 1. Clone and Setup

```bash
git clone https://github.com/soumyachk101/IdeaForge.git
cd IdeaForge

# Backend setup
cd backend
cp .env.example .env
uv sync
```

### 2. Seed the Knowledge Base

```bash
cd backend
uv run python -m rag.ingest
```

```
Ingesting seed data...
  monetization_frameworks: 7 documents, 7 chunks
  pain_points: 12 documents, 12 chunks
  startup_case_studies: 7 documents, 7 chunks
Done! Total: 26 documents in 3 collections
```

### 3. Start Everything

```bash
# Terminal 1 - Backend
cd backend
uv run uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Ollama
ollama pull deepseek-coder-v2
ollama serve

# Terminal 3 - Frontend
cd frontend
npm install && npm run dev
```

### 4. Generate Ideas

Open **http://localhost:3000** -> Select a niche -> Click **Generate Ideas** -> Watch the 3 agents work in real-time via SSE streaming.

---

## API

```mermaid
graph LR
    subgraph ENDPOINTS["REST API Endpoints"]
        direction TB
        H["GET /api/health"]
        S["GET /api/stats"]
        IG["POST /api/ideas/generate - SSE"]
        IL["GET /api/ideas"]
        IID["GET /api/ideas/:id"]
        TL["GET /api/trends"]
        TS["POST /api/trends/scrape"]
        RQ["POST /api/rag/query"]
        RI["POST /api/rag/ingest/seed"]
        RB["GET /api/rag/browse/:collection"]
        DOC["GET /docs - Swagger UI"]
    end

    style H fill:#4CAF50,color:#fff
    style S fill:#4CAF50,color:#fff
    style IG fill:#2196F3,color:#fff
    style IL fill:#2196F3,color:#fff
    style IID fill:#2196F3,color:#fff
    style TL fill:#FF9800,color:#fff
    style TS fill:#FF9800,color:#fff
    style RQ fill:#9C27B0,color:#fff
    style RI fill:#9C27B0,color:#fff
    style RB fill:#9C27B0,color:#fff
    style DOC fill:#607D8B,color:#fff
```

### Generate Ideas (SSE Stream)

```bash
curl -N -X POST http://127.0.0.1:8000/api/ideas/generate \
  -H "Content-Type: application/json" \
  -d '{"niche": "developer tools"}'
```

```
data: {"type":"start","niche":"developer tools","id":"a1b2c3d4"}
data: {"type":"result","id":"a1b2c3d4","content":"## LogLens AI\n\n### The Problem\n..."}
data: {"type":"done","id":"a1b2c3d4"}
```

### Search RAG Knowledge Base

```bash
curl -X POST http://127.0.0.1:8000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "developer tools for log analysis", "collection": "all"}'
```

---

## Knowledge Base (RAG)

### Hybrid Retrieval Pipeline

```mermaid
flowchart TB
    Q["Query: developer tools for log analysis"]

    subgraph SEARCH["Dual Search"]
        VS["Vector Search - ChromaDB cosine similarity"]
        BM["BM25 Search - TF-IDF keyword matching"]
    end

    FUSION["Reciprocal Rank Fusion - score = sum of 1/(k+rank)"]

    RANK["Ranked Results"]

    Q --> VS
    Q --> BM
    VS --> FUSION
    BM --> FUSION
    FUSION --> RANK

    style Q fill:#4CAF50,stroke:#388E3C,color:#fff
    style VS fill:#2196F3,stroke:#1565C0,color:#fff
    style BM fill:#FF9800,stroke:#E65100,color:#fff
    style FUSION fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style RANK fill:#607D8B,stroke:#37474F,color:#fff
```

### Seed Data

| Collection | Docs | Description |
|------------|------|-------------|
| `monetization_frameworks` | 7 | Freemium, API-as-a-service, Subscription, etc. |
| `pain_points` | 12 | "I wish there was a tool that..." complaints |
| `startup_case_studies` | 7 | Real micro-SaaS with revenue and tech stacks |

---

## LLM Configuration

```mermaid
flowchart LR
    ENV[".env - LLM_PROVIDER"] --> CONFIG["config.py - reads env"]
    CONFIG --> CLIENT["ollama_client.py - get_crewai_llm"]
    CLIENT --> AGENT["CrewAI Agent .llm = LLM"]

    subgraph PROVIDERS["Supported Providers"]
        O["Ollama - deepseek-coder-v2 / llama3 / mistral"]
        A["Anthropic - claude-sonnet-4"]
    end

    CLIENT --> O
    CLIENT --> A

    style ENV fill:#607D8B,color:#fff
    style O fill:#4CAF50,stroke:#388E3C,color:#fff
    style A fill:#2196F3,stroke:#1565C0,color:#fff
```

| Provider | Model | Use Case |
|----------|-------|----------|
| Ollama | `deepseek-coder-v2` | Best for local dev (coding) |
| Ollama | `llama3` | Good general purpose |
| Ollama | `mistral` | Fast, decent quality |
| Anthropic | `claude-sonnet-4` | Production quality |

---

## Project Structure

```
IdeaForge/
|
+-- backend/                          # Python backend
|   +-- pyproject.toml                # Dependencies & project config
|   +-- .env.example                  # Environment variables template
|   +-- config.py                     # Centralized configuration
|   +-- main.py                       # CLI: serve | ingest | generate | scrape
|   |
|   +-- agents/                       # CrewAI 3-agent pipeline
|   |   +-- crew.py                   #   Orchestrates sequential flow
|   |   +-- trend_scraper.py          #   Agent 1: scrapes 4 sources
|   |   +-- synthesizer.py            #   Agent 2: RAG gap analysis
|   |   +-- vc_agent.py               #   Agent 3: business proposals
|   |
|   +-- scrapers/                     # Data source scrapers
|   |   +-- base.py                   #   TrendData model + BaseScraper
|   |   +-- hacker_news.py            #   HN Firebase API
|   |   +-- reddit.py                 #   PRAW (5 subreddits)
|   |   +-- product_hunt.py           #   GraphQL API + fallback
|   |   +-- indie_hackers.py          #   BeautifulSoup scraping
|   |
|   +-- rag/                          # RAG pipeline
|   |   +-- embedder.py               #   SentenceTransformers (MPS/CPU)
|   |   +-- chroma_client.py          #   ChromaDB (4 collections)
|   |   +-- retriever.py              #   Hybrid vector+BM25+RRF
|   |   +-- ingest.py                 #   Seed data ingestion
|   |   +-- seed_data/                #   Pre-built knowledge base
|   |
|   +-- llm/                          # LLM layer
|   |   +-- ollama_client.py          #   Ollama + Anthropic + CrewAI
|   |   +-- prompts.py                #   System prompts for agents
|   |
|   +-- tools/                        # CrewAI tools
|   |   +-- scraper_tools.py          #   Scrapers as BaseTool
|   |   +-- rag_tools.py              #   RAG as BaseTool
|   |
|   +-- api/                          # FastAPI backend
|       +-- main.py                   #   App + CORS + lifespan
|       +-- models.py                 #   Pydantic models
|       +-- routes/
|           +-- health.py             #   /api/health, /api/stats
|           +-- ideas.py              #   /api/ideas/generate (SSE)
|           +-- trends.py             #   /api/trends/scrape
|           +-- rag.py                #   /api/rag/query, /browse
|
+-- frontend/                         # Next.js 14 dashboard
    +-- next.config.ts                # API proxy to :8000
    +-- lib/api.ts                    # API client
    +-- app/
        +-- layout.tsx                # Navigation + layout
        +-- page.tsx                  # Generate (SSE streaming)
        +-- ideas/                    # Ideas gallery + detail
        +-- trends/page.tsx           # Trend browser
        +-- knowledge/page.tsx        # RAG search + browse
```

---

## Troubleshooting

<details>
<summary><b>"ModuleNotFoundError: No module named 'agents'"</b></summary>

```bash
# Always run from the backend/ directory:
cd IdeaForge/backend
uv run python -m rag.ingest
```
</details>

<details>
<summary><b>"Ollama connection refused"</b></summary>

```bash
# Start Ollama first:
ollama serve
ollama pull deepseek-coder-v2
```
</details>

<details>
<summary><b>"No results from Reddit scraper"</b></summary>

Reddit requires API credentials. Go to https://www.reddit.com/prefs/apps, create a "script" app, and add to `.env`:
```bash
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
```
</details>

<details>
<summary><b>"TextEmbedder takes 30+ seconds to load"</b></summary>

First load downloads the model (~80MB). Subsequent loads use cache. Apple Silicon MPS acceleration is auto-detected.
</details>

<details>
<summary><b>"ChromaDB collection not found"</b></summary>

```bash
cd IdeaForge/backend
uv run python -m rag.ingest --reset
```
</details>

<details>
<summary><b>Frontend shows "Failed to fetch"</b></summary>

```bash
# Check backend is running:
curl http://127.0.0.1:8000/api/health

# If not:
cd IdeaForge/backend
uv run uvicorn api.main:app --reload
```
</details>

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `ollama` | `ollama` or `anthropic` |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `deepseek-coder-v2` | Ollama model name |
| `ANTHROPIC_API_KEY` | -- | Only if LLM_PROVIDER=anthropic |
| `REDDIT_CLIENT_ID` | -- | Reddit API credentials |
| `REDDIT_CLIENT_SECRET` | -- | Reddit API credentials |
| `PRODUCT_HUNT_TOKEN` | -- | PH GraphQL API token |
| `CHROMA_PATH` | `.ideaforge_data/chroma` | ChromaDB storage path |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model |
| `API_HOST` | `127.0.0.1` | Backend host |
| `API_PORT` | `8000` | Backend port |

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

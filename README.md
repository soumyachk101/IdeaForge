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

### High-Level Data Flow

```mermaid
graph LR
    A["User selects niche"] --> B["Trend Scraper"]
    B --> C["Synthesizer"]
    C --> D["VC Advisor"]
    D --> E["Business Proposals"]

    F["Product Hunt"] --> B
    G["Hacker News"] --> B
    H["Reddit"] --> B
    I["Indie Hackers"] --> B

    J["ChromaDB"] --> C
    K["BM25 Index"] --> C

    style A fill:#4CAF50,stroke:#388E3C,color:#fff
    style B fill:#2196F3,stroke:#1565C0,color:#fff
    style C fill:#FF9800,stroke:#E65100,color:#fff
    style D fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style E fill:#4CAF50,stroke:#388E3C,color:#fff
    style F fill:#607D8B,stroke:#37474F,color:#fff
    style G fill:#607D8B,stroke:#37474F,color:#fff
    style H fill:#607D8B,stroke:#37474F,color:#fff
    style I fill:#607D8B,stroke:#37474F,color:#fff
    style J fill:#607D8B,stroke:#37474F,color:#fff
    style K fill:#607D8B,stroke:#37474F,color:#fff
```

### Agent Pipeline Sequence

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
    A1->>A1: Scrape Reddit
    A1->>A1: Scrape Indie Hackers
    A1-->>A2: Trend report + pain points
    deactivate A1

    activate A2
    A2->>DB: Vector search
    A2->>DB: BM25 keyword search
    DB-->>A2: Frameworks + case studies
    A2->>A2: Reciprocal Rank Fusion
    A2-->>A3: Ranked opportunities
    deactivate A2

    activate A3
    A3->>A3: Generate product name
    A3->>A3: Select tech stack
    A3->>A3: Define pricing
    A3->>A3: Create GTM strategy
    A3-->>U: 3-5 proposals via SSE
    deactivate A3
```

### Agent Execution State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> TrendScraping : User selects niche
    TrendScraping --> TrendComplete : All 4 sources scraped
    TrendComplete --> RAGSearch : Pass trends to Synthesizer
    RAGSearch --> RAGComplete : Hybrid search done
    RAGComplete --> ProposalGen : Pass insights to VC Advisor
    ProposalGen --> Streaming : Generate proposals
    Streaming --> Complete : All proposals sent
    Complete --> [*]

    TrendScraping --> Error : Scraper fails
    RAGSearch --> Error : ChromaDB fails
    ProposalGen --> Error : LLM fails
    Error --> Idle : Reset
```

---

## Architecture

```
IDEAFORGE ARCHITECTURE
======================

+-----------------------------------------------------------------------+
|                        FRONTEND (Next.js)                              |
|                                                                       |
|  +------------+  +------------+  +------------+  +-----------------+  |
|  | Generate   |  |  Ideas     |  |  Trends    |  | Knowledge Base  |  |
|  |  Page      |  | Gallery    |  | Browser    |  | (Search/Browse) |  |
|  +-----+------+  +-----+------+  +-----+------+  +--------+--------+  |
|        |               |              |                    |           |
|        +---------------+--------------+--------------------+           |
|                        |                                               |
|                +-------+--------+                                      |
|                |   API Client   |                                      |
|                |   (lib/api.ts) |                                      |
|                +-------+--------+                                      |
|                        |                                               |
|                +-------+--------+                                      |
|                |  Next.js Proxy |                                      |
|                | /api/* -> :8000|                                      |
|                +-------+--------+                                      |
+------------------------+-----------------------------------------------+
                         |
                         | HTTP + SSE
                         |
+------------------------+-----------------------------------------------+
|                        |      BACKEND (FastAPI + CrewAI)               |
|                +-------+--------+                                      |
|                |   FastAPI App  |                                      |
|                |   (api/main)   |                                      |
|                +-------+--------+                                      |
|                        |                                               |
|    +-------------------+-------------------+                            |
|    |                   |                   |                            |
|    v                   v                   v                            |
| +--------+    +------------+    +-------------+                        |
| | Ideas  |    |  Trends    |    |    RAG      |                        |
| | Route  |    |  Route     |    |   Route     |                        |
| +---+----+    +-----+------+    +------+------+                        |
|     |               |                    |                              |
|     v               v                    v                              |
| +--------------------------------------------------------------+       |
| |                   CREWAI ORCHESTRATION                       |       |
| |                                                              |       |
| |  +----------+  +--------------+  +---------------------+    |       |
| |  | Trend    |  | Synthesizer  |  |  VC/Monetization    |    |       |
| |  | Scraper  |  | Agent        |  |  Advisor            |    |       |
| |  | Agent    |  |              |  |                     |    |       |
| |  +----+-----+  +------+-------+  +----------+----------+    |       |
| |       |               |                     |               |       |
| |       v               v                     v               |       |
| |  +----------+  +--------------+  +---------------------+    |       |
| |  | Scraper  |  | RAG Retriever|  |  System Prompts     |    |       |
| |  | Tools    |  | Tool         |  |                     |    |       |
| |  +----+-----+  +------+-------+  +---------------------+    |       |
| +-------+---------------+--------------------------------------+       |
|         |               |                                              |
|         v               v                                              |
|  +------------+  +--------------+                                      |
|  | SCRAPERS   |  |  RAG PIPELINE|                                      |
|  |            |  |              |                                      |
|  | - HN API   |  | - ChromaDB   |                                      |
|  | - Reddit   |  | - BM25       |                                      |
|  | - PH API   |  | - Embeddings |                                      |
|  | - IH HTML  |  | - RRF Fusion |                                      |
|  +------------+  +--------------+                                      |
+-----------------------------------------------------------------------+
```

### System Component Diagram

```mermaid
graph TB
    subgraph FE["Frontend - Next.js 14"]
        P1["Generate Page"]
        P2["Ideas Gallery"]
        P3["Trends Browser"]
        P4["Knowledge Search"]
        P1 --> API["API Client"]
        P2 --> API
        P3 --> API
        P4 --> API
        API --> PROXY["Next.js Proxy to :8000"]
    end

    subgraph BE["Backend - FastAPI + CrewAI"]
        PROXY --> FAST["FastAPI App"]
        FAST --> R1["Ideas Route"]
        FAST --> R2["Trends Route"]
        FAST --> R3["RAG Route"]

        subgraph CREW["CrewAI Agents"]
            A1["Trend Scraper"]
            A2["Synthesizer"]
            A3["VC Advisor"]
            A1 --> A2 --> A3
        end

        R1 --> CREW
    end

    subgraph DATA["Data Layer"]
        A1 --> SC["Scrapers"]
        A2 --> RAG["RAG Pipeline"]
        SC --> S1["HN API"]
        SC --> S2["Reddit PRAW"]
        SC --> S3["PH GraphQL"]
        SC --> S4["IH HTML"]
        RAG --> DB[("ChromaDB")]
        RAG --> BM["BM25 Index"]
        RAG --> EM["Embeddings"]
    end

    subgraph LLM["LLM Providers"]
        A3 --> L1["Ollama"]
        A3 --> L2["Anthropic"]
    end

    style FE fill:#e3f2fd,stroke:#1565C0
    style BE fill:#fff3e0,stroke:#E65100
    style DATA fill:#f3e5f5,stroke:#6A1B9A
    style LLM fill:#e8f5e9,stroke:#2E7D32
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS | Dashboard + SSE streaming |
| **Backend** | FastAPI, CrewAI, Pydantic, uvicorn | API + multi-agent orchestration |
| **AI / ML** | Ollama, Anthropic Claude, SentenceTransformers, ChromaDB | LLM serving, embeddings, vector DB |
| **Scrapers** | httpx, PRAW, BeautifulSoup4, Product Hunt GraphQL | 4-source trend scraping |
| **Hybrid Search** | BM25 + Reciprocal Rank Fusion | Vector + keyword search merging |
| **Package Mgmt** | uv (Python), npm (Node.js) | Fast deterministic installs |

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

### Setup Flow

```mermaid
graph TD
    A["Clone repo"] --> B["cd backend"]
    B --> C["cp .env.example .env"]
    C --> D["uv sync"]
    D --> E["uv run python -m rag.ingest"]
    E --> F["Start backend on :8000"]
    F --> G["Start Ollama"]
    G --> H["cd frontend && npm install && npm run dev"]
    H --> I["Open localhost:3000"]

    style A fill:#4CAF50,color:#fff
    style I fill:#2196F3,color:#fff
```

---

## API

### Endpoint Map

```mermaid
graph TD
    subgraph HEALTH["Health"]
        H1["GET /api/health"]
        H2["GET /api/stats"]
    end

    subgraph IDEAS["Ideas"]
        I1["POST /api/ideas/generate"]
        I2["GET /api/ideas"]
        I3["GET /api/ideas/:id"]
    end

    subgraph TRENDS["Trends"]
        T1["GET /api/trends"]
        T2["POST /api/trends/scrape"]
    end

    subgraph RAG["RAG"]
        R1["POST /api/rag/query"]
        R2["POST /api/rag/ingest/seed"]
        R3["GET /api/rag/browse/:col"]
    end

    DOCS["GET /docs - Swagger UI"]

    style HEALTH fill:#4CAF50,color:#fff
    style IDEAS fill:#2196F3,color:#fff
    style TRENDS fill:#FF9800,color:#fff
    style RAG fill:#9C27B0,color:#fff
    style DOCS fill:#607D8B,color:#fff
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

### SSE Event Flow

```mermaid
graph LR
    A["Client POST /api/ideas/generate"] --> B["FastAPI receives request"]
    B --> C["CrewAI starts agents"]
    C --> D["SSE: type=start"]
    D --> E["Agent 1 scrapes trends"]
    E --> F["Agent 2 searches RAG"]
    F --> G["Agent 3 generates proposals"]
    G --> H["SSE: type=result"]
    H --> I["SSE: type=done"]
    I --> J["Client renders results"]

    style A fill:#2196F3,color:#fff
    style D fill:#FF9800,color:#fff
    style H fill:#4CAF50,color:#fff
    style I fill:#9C27B0,color:#fff
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
graph TB
    Q["Query: developer tools for log analysis"] --> VS["Vector Search"]
    Q --> BM["BM25 Search"]
    VS --> F["Reciprocal Rank Fusion"]
    BM --> F
    F --> R["Ranked Results"]

    style Q fill:#4CAF50,stroke:#388E3C,color:#fff
    style VS fill:#2196F3,stroke:#1565C0,color:#fff
    style BM fill:#FF9800,stroke:#E65100,color:#fff
    style F fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style R fill:#607D8B,stroke:#37474F,color:#fff
```

### RAG Data Model

```mermaid
classDiagram
    class TrendData {
        +String title
        +String description
        +String source
        +List tags
        +int upvotes
        +String url
    }

    class Document {
        +String id
        +String content
        +String title
        +String category
        +String source
        +float[] embedding
    }

    class QueryResult {
        +String document_id
        +float score
        +String content
        +dict metadata
    }

    class Retriever {
        +ChromaDB client
        +BM25 index
        +search(query, collection)
        +hybrid_search(query, collection)
    }

    Document --> Retriever : indexed by
    TrendData --> Document : converted to
    Retriever --> QueryResult : returns
```

### Seed Data

| Collection | Docs | Description |
|------------|------|-------------|
| `monetization_frameworks` | 7 | Freemium, API-as-a-service, Subscription, etc. |
| `pain_points` | 12 | "I wish there was a tool that..." complaints |
| `startup_case_studies` | 7 | Real micro-SaaS with revenue and tech stacks |

---

## LLM Configuration

### Provider Selection Flow

```mermaid
graph LR
    ENV[".env file"] --> CONFIG["config.py"]
    CONFIG --> CLIENT["ollama_client.py"]
    CLIENT --> CHECK{"LLM_PROVIDER?"}
    CHECK -->|ollama| O["Ollama Server"]
    CHECK -->|anthropic| A["Anthropic API"]
    O --> AGENT["CrewAI Agent"]
    A --> AGENT

    style ENV fill:#607D8B,color:#fff
    style CHECK fill:#FF9800,color:#fff
    style O fill:#4CAF50,color:#fff
    style A fill:#2196F3,color:#fff
    style AGENT fill:#9C27B0,color:#fff
```

### Model Options

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

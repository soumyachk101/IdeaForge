# IdeaForge Frontend

Next.js 14 dashboard for the IdeaForge multi-agent idea discovery engine.

## Pages

| Route         | Description                          |
|---------------|--------------------------------------|
| `/`           | Generate ideas with niche selector   |
| `/ideas`      | Browse generated idea proposals      |
| `/ideas/[id]` | View individual idea detail          |
| `/trends`     | Scrape & browse trends by source     |
| `/knowledge`  | Search & browse RAG knowledge base   |

## Setup

```bash
npm install
npm run dev
```

Runs on `http://localhost:3000`. API calls are proxied to `http://127.0.0.1:8000` via `next.config.ts` rewrites.

## Tech Stack

- **Next.js 14** (App Router)
- **TypeScript** 
- **Tailwind CSS 4**
- **SSE streaming** via `fetch` + `ReadableStream`

## Key Files

- `lib/api.ts` — API client with typed interfaces and SSE streaming
- `app/layout.tsx` — Root layout with navigation
- `app/page.tsx` — Generate page (niche selector + SSE output)
- `next.config.ts` — API proxy configuration

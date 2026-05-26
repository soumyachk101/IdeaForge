const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export interface IdeaSummary {
  id: string;
  niche: string;
  preview: string;
  created_at: string;
}

export interface IdeaResponse {
  id: string;
  niche: string;
  content: string;
  created_at: string;
  status: string;
}

export interface TrendData {
  source: string;
  title: string;
  description: string;
  url: string;
  upvotes: number;
  comments_count: number;
  tags: string[];
}

export interface RAGResult {
  id: string;
  text: string;
  metadata: Record<string, unknown>;
  score: number;
  collection?: string;
}

export async function fetchIdeas(): Promise<IdeaSummary[]> {
  const res = await fetch(`${API_BASE}/api/ideas`);
  if (!res.ok) throw new Error("Failed to fetch ideas");
  return res.json();
}

export async function fetchIdea(id: string): Promise<IdeaResponse> {
  const res = await fetch(`${API_BASE}/api/ideas/${id}`);
  if (!res.ok) throw new Error("Idea not found");
  return res.json();
}

export async function fetchTrends(
  source = "all",
  limit = 20
): Promise<TrendData[]> {
  const res = await fetch(
    `${API_BASE}/api/trends?source=${source}&limit=${limit}`
  );
  if (!res.ok) throw new Error("Failed to fetch trends");
  return res.json();
}

export async function scrapeTrends(
  source = "all",
  limit = 20
): Promise<{ message: string; sources: string[] }> {
  const res = await fetch(
    `${API_BASE}/api/trends/scrape?source=${source}&limit=${limit}`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error("Failed to scrape trends");
  return res.json();
}

export async function queryRAG(
  query: string,
  collection = "all",
  nResults = 5
): Promise<{ results: Record<string, RAGResult[]> }> {
  const res = await fetch(`${API_BASE}/api/rag/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, collection, n_results: nResults }),
  });
  if (!res.ok) throw new Error("RAG query failed");
  return res.json();
}

export async function ingestSeedData(
  reset = false
): Promise<{ message: string }> {
  const res = await fetch(
    `${API_BASE}/api/rag/ingest/seed?reset=${reset}`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error("Ingestion failed");
  return res.json();
}

export function streamIdeas(
  niche: string,
  onEvent: (event: Record<string, unknown>) => void,
  onError: (error: Error) => void
): () => void {
  const controller = new AbortController();

  fetch(`${API_BASE}/api/ideas/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ niche }),
    signal: controller.signal,
  })
    .then(async (res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const reader = res.body?.getReader();
      if (!reader) return;

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));
              onEvent(data);
            } catch {
              // skip malformed JSON
            }
          }
        }
      }
    })
    .catch((err) => {
      if (err.name !== "AbortError") onError(err);
    });

  return () => controller.abort();
}

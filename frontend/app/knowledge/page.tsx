"use client";

import { useState } from "react";
import { queryRAG, ingestSeedData } from "@/lib/api";
import type { RAGResult } from "@/lib/api";

const COLLECTIONS = [
  { value: "all", label: "All Collections" },
  { value: "pain_points", label: "Pain Points" },
  { value: "monetization_frameworks", label: "Monetization Frameworks" },
  { value: "startup_case_studies", label: "Case Studies" },
];

export default function KnowledgePage() {
  const [query, setQuery] = useState("");
  const [collection, setCollection] = useState("all");
  const [results, setResults] = useState<Record<string, RAGResult[]> | null>(null);
  const [loading, setLoading] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [ingestMsg, setIngestMsg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await queryRAG(query, collection, 5);
      setResults(data.results);
    } catch (err: any) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleIngest = async (reset: boolean) => {
    setIngesting(true);
    setIngestMsg(null);
    setError(null);
    try {
      const data = await ingestSeedData(reset);
      setIngestMsg(data.message);
    } catch (err: any) {
      setError(err.message);
    }
    setIngesting(false);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-2">Knowledge Base</h1>
      <p className="text-zinc-500 mb-8">
        Search monetization frameworks, user pain points, and startup case studies stored in the RAG database.
      </p>

      {/* Ingest seed data */}
      <div className="mb-8 p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950">
        <h2 className="text-sm font-semibold mb-3">Seed Data</h2>
        <p className="text-xs text-zinc-500 mb-4">
          Ingest pre-built knowledge base with monetization frameworks, pain points, and case studies.
        </p>
        <div className="flex gap-3">
          <button
            onClick={() => handleIngest(false)}
            disabled={ingesting}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 disabled:opacity-50 transition-colors"
          >
            {ingesting ? "Ingesting..." : "Ingest Seed Data"}
          </button>
          <button
            onClick={() => handleIngest(true)}
            disabled={ingesting}
            className="px-4 py-2 rounded-lg text-sm font-medium border border-red-300 dark:border-red-700 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 disabled:opacity-50 transition-colors"
          >
            Reset &amp; Re-ingest
          </button>
        </div>
        {ingestMsg && (
          <p className="mt-3 text-sm text-green-600 dark:text-green-400">{ingestMsg}</p>
        )}
      </div>

      {/* Search */}
      <div className="mb-8">
        <div className="flex gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder="Search... e.g., 'developer log analysis' or 'healthcare pain points'"
            className="flex-1 px-4 py-3 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-900 dark:focus:ring-zinc-100"
          />
          <select
            value={collection}
            onChange={(e) => setCollection(e.target.value)}
            className="px-4 py-3 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 text-sm"
          >
            {COLLECTIONS.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
          <button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="px-6 py-3 rounded-lg font-medium bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 disabled:opacity-50 transition-colors"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300">
          {error}
        </div>
      )}

      {/* Results */}
      {results && Object.keys(results).length > 0 && (
        <div className="space-y-8">
          {Object.entries(results).map(([colName, docs]) => (
            <div key={colName}>
              <h2 className="text-lg font-semibold mb-4 capitalize">
                {colName.replace(/_/g, " ")}
              </h2>
              <div className="space-y-3">
                {docs.map((doc, i) => (
                  <div
                    key={i}
                    className="p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950"
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-xs font-mono px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500">
                        score: {(doc as RAGResult & { score?: number }).score?.toFixed(4) ?? "N/A"}
                      </span>
                      {doc.metadata?.title != null && (
                        <span className="text-sm font-medium">{String(doc.metadata.title)}</span>
                      )}
                      {doc.metadata?.category != null && (
                        <span className="text-xs text-zinc-500">{String(doc.metadata.category)}</span>
                      )}
                    </div>
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                      {doc.text}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {results && Object.keys(results).length === 0 && (
        <div className="text-center py-12 text-zinc-500">
          No results found. Try a different query.
        </div>
      )}
    </div>
  );
}

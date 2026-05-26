"use client";

import { useState, useEffect } from "react";
import { fetchTrends, scrapeTrends } from "@/lib/api";
import type { TrendData } from "@/lib/api";

const SOURCE_LABELS: Record<string, string> = {
  hacker_news: "Hacker News",
  reddit: "Reddit",
  product_hunt: "Product Hunt",
  indie_hackers: "Indie Hackers",
};

const SOURCE_COLORS: Record<string, string> = {
  hacker_news: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400",
  reddit: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  product_hunt: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
  indie_hackers: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
};

export default function TrendsPage() {
  const [trends, setTrends] = useState<TrendData[]>([]);
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchTrends("all", 50)
      .then(setTrends)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleScrape = async (source = "all") => {
    setScraping(true);
    setError(null);
    try {
      await scrapeTrends(source, 20);
      const fresh = await fetchTrends("all", 50);
      setTrends(fresh);
    } catch (err: any) {
      setError(err.message);
    }
    setScraping(false);
  };

  const filtered = filter === "all" ? trends : trends.filter((t) => t.source === filter);

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Trends</h1>
          <p className="text-zinc-500">
            Latest trends from Product Hunt, Hacker News, Reddit, and Indie Hackers.
          </p>
        </div>
        <button
          onClick={() => handleScrape("all")}
          disabled={scraping}
          className="px-5 py-2.5 rounded-lg font-medium bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 disabled:opacity-50 transition-colors"
        >
          {scraping ? "Scraping..." : "Scrape All Sources"}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300">
          {error}
        </div>
      )}

      {/* Source filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {["all", "hacker_news", "reddit", "product_hunt", "indie_hackers"].map((source) => (
          <button
            key={source}
            onClick={() => setFilter(source)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              filter === source
                ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
                : "bg-zinc-100 text-zinc-700 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
            }`}
          >
            {source === "all" ? "All" : SOURCE_LABELS[source]}
          </button>
        ))}
      </div>

      {/* Individual scrape buttons */}
      <div className="flex flex-wrap gap-2 mb-8">
        {["hacker_news", "reddit", "product_hunt", "indie_hackers"].map((source) => (
          <button
            key={source}
            onClick={() => handleScrape(source)}
            disabled={scraping}
            className="px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-50 transition-colors"
          >
            Scrape {SOURCE_LABELS[source]}
          </button>
        ))}
      </div>

      {loading && (
        <div className="flex items-center gap-3 text-zinc-500 py-12">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          Loading trends...
        </div>
      )}

      {!loading && filtered.length === 0 && (
        <div className="text-center py-16 border border-dashed border-zinc-300 dark:border-zinc-700 rounded-xl">
          <p className="text-zinc-500 mb-2">No trends loaded yet.</p>
          <p className="text-sm text-zinc-400">Click &ldquo;Scrape All Sources&rdquo; to fetch the latest data.</p>
        </div>
      )}

      <div className="space-y-3">
        {filtered.map((trend, i) => (
          <div
            key={i}
            className="p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 hover:border-zinc-400 dark:hover:border-zinc-600 bg-white dark:bg-zinc-950 transition-colors"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${SOURCE_COLORS[trend.source] || "bg-zinc-100 text-zinc-700"}`}>
                    {SOURCE_LABELS[trend.source] || trend.source}
                  </span>
                  {trend.upvotes > 0 && (
                    <span className="text-xs text-zinc-400">{trend.upvotes} pts</span>
                  )}
                </div>
                <a
                  href={trend.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-base font-medium hover:underline block mb-1"
                >
                  {trend.title}
                </a>
                {trend.description && (
                  <p className="text-sm text-zinc-500 line-clamp-2">{trend.description}</p>
                )}
                {trend.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {trend.tags.map((tag, j) => (
                      <span key={j} className="text-xs px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              {trend.comments_count > 0 && (
                <span className="text-xs text-zinc-400 shrink-0">
                  {trend.comments_count} comments
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { fetchIdea } from "@/lib/api";
import type { IdeaResponse } from "@/lib/api";

export default function IdeaDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [idea, setIdea] = useState<IdeaResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchIdea(id)
      .then(setIdea)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center text-zinc-500">
        Loading...
      </div>
    );
  }

  if (error || !idea) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center text-red-500">
        {error || "Idea not found"}
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <span className="inline-block px-2 py-1 text-xs font-medium rounded-md bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
            {idea.niche}
          </span>
        </div>
        <span className="text-sm text-zinc-400">
          {new Date(idea.created_at).toLocaleString()}
        </span>
      </div>

      <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-8">
        <article className="prose dark:prose-invert max-w-none">
          <div className="whitespace-pre-wrap font-mono text-sm leading-relaxed">
            {idea.content}
          </div>
        </article>
      </div>
    </div>
  );
}

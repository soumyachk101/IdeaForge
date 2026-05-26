"use client";

import { useState, useRef } from "react";
import { streamIdeas } from "@/lib/api";

const NICHES = [
  "developer tools",
  "productivity",
  "marketing tools",
  "legal tech",
  "healthcare",
  "real estate",
  "freelancer tools",
  "education",
  "e-commerce",
  "local business tools",
];

export default function GeneratePage() {
  const [niche, setNiche] = useState("developer tools");
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState("");
  const [ideaId, setIdeaId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const outputRef = useRef<HTMLDivElement>(null);

  const handleGenerate = () => {
    setIsRunning(true);
    setOutput("");
    setIdeaId(null);
    setError(null);

    const cancel = streamIdeas(
      niche,
      (event) => {
        if (event.type === "start") {
          setOutput(`Starting IdeaForge pipeline for "${niche}"...\n\n`);
        } else if (event.type === "progress") {
          setOutput(
            (prev) =>
              prev +
              `[${event.agent}] ${event.status}\n`
          );
        } else if (event.type === "result") {
          setOutput((prev) => prev + "\n" + (event.content as string));
          setIdeaId(event.id as string);
        } else if (event.type === "error") {
          setError(event.message as string);
        } else if (event.type === "done") {
          setIsRunning(false);
        }
      },
      (err) => {
        setError(err.message);
        setIsRunning(false);
      }
    );

    return cancel;
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      {/* Hero */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold tracking-tight mb-4">
          Discover Your Next Micro-SaaS
        </h1>
        <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
          Our 3-agent AI system scrapes real-time trends, matches them with
          proven monetization frameworks, and generates actionable business
          proposals.
        </p>
      </div>

      {/* Niche Selector */}
      <div className="mb-8">
        <label className="block text-sm font-medium mb-3">Select a Niche</label>
        <div className="flex flex-wrap gap-2">
          {NICHES.map((n) => (
            <button
              key={n}
              onClick={() => setNiche(n)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                niche === n
                  ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
                  : "bg-zinc-100 text-zinc-700 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
              }`}
            >
              {n}
            </button>
          ))}
        </div>
      </div>

      {/* Generate Button */}
      <div className="mb-8">
        <button
          onClick={handleGenerate}
          disabled={isRunning}
          className="w-full py-4 px-6 rounded-xl text-lg font-semibold bg-zinc-900 text-white hover:bg-zinc-800 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 transition-colors"
        >
          {isRunning ? (
            <span className="flex items-center justify-center gap-3">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Agents Working...
            </span>
          ) : (
            "Generate Ideas"
          )}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-8 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300">
          {error}
        </div>
      )}

      {/* Output */}
      {(output || isRunning) && (
        <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 overflow-hidden">
          <div className="bg-zinc-100 dark:bg-zinc-800 px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div
                className={`w-3 h-3 rounded-full ${
                  isRunning
                    ? "bg-green-500 animate-pulse"
                    : "bg-zinc-400"
                }`}
              />
              <span className="text-sm font-medium">
                {isRunning ? "Pipeline Running" : "Pipeline Complete"}
              </span>
            </div>
            {ideaId && (
              <a
                href={`/ideas/${ideaId}`}
                className="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
              >
                View Saved Idea
              </a>
            )}
          </div>
          <div
            ref={outputRef}
            className="p-6 max-h-[600px] overflow-y-auto bg-white dark:bg-zinc-900"
          >
            <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed">
              {output}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

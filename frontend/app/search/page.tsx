"use client";

import { useState } from "react";
import { searchCode } from "../lib/api";

interface SearchResult {
  content: string;
  source: string;
  score: number;
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResults([]);
    setSearched(true);

    try {
      const data = await searchCode(query);
      setResults(data.results);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">
          <span className="gradient-text">Semantic</span> Code Search
        </h1>
        <p className="text-[var(--muted)]">
          Search your indexed codebase using natural language. Find relevant
          code by describing what you&apos;re looking for.
        </p>
      </div>

      <form onSubmit={handleSearch} className="mb-8">
        <div className="card p-6">
          <label className="block text-sm font-medium mb-2 text-[var(--muted)]">
            Search Query
          </label>
          <div className="flex gap-3">
            <input
              className="input-field flex-1"
              placeholder="e.g. user authentication logic, database connection, error handling"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button
              type="submit"
              className="btn-primary flex items-center gap-2 whitespace-nowrap"
              disabled={loading || !query.trim()}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Searching...
                </>
              ) : (
                <>
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                  Search
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {error && (
        <div className="card p-4 mb-6 border-[var(--danger)]">
          <p className="text-[var(--danger)] text-sm">{error}</p>
        </div>
      )}

      {searched && !loading && (
        <div className="mb-4 text-sm text-[var(--muted)]">
          Found <span className="text-white font-medium">{total}</span> results
        </div>
      )}

      {results.length > 0 && (
        <div className="space-y-4">
          {results.map((result, i) => (
            <div key={i} className="card p-5">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <svg
                    className="w-4 h-4 text-[var(--accent)]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <span className="text-sm font-medium text-[var(--accent)]">
                    {result.source}
                  </span>
                </div>
                {result.score !== undefined && (
                  <span className="text-xs bg-[var(--background)] text-[var(--muted)] px-2 py-1 rounded border border-[var(--border)]">
                    Score: {(result.score * 100).toFixed(1)}%
                  </span>
                )}
              </div>
              <div className="code-block text-sm">{result.content}</div>
            </div>
          ))}
        </div>
      )}

      {searched && !loading && results.length === 0 && !error && (
        <div className="card p-8 text-center">
          <svg
            className="w-12 h-12 mx-auto mb-3 text-[var(--muted)] opacity-30"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          <p className="text-[var(--muted)] text-sm">
            No results found. Try a different query or index more repositories.
          </p>
        </div>
      )}
    </div>
  );
}

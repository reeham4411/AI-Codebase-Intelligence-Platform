"use client";

import { useState } from "react";
import { askQuestion } from "./lib/api";

export default function AskPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const data = await askQuestion(question);
      setAnswer(data.answer);
      setSources(data.sources);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get answer");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">
          <span className="gradient-text">Ask AI</span> about your codebase
        </h1>
        <p className="text-[var(--muted)]">
          Ask questions about your indexed repositories. The AI will search
          through the code and provide intelligent answers.
        </p>
      </div>

      <form onSubmit={handleAsk} className="mb-8">
        <div className="card p-6">
          <label className="block text-sm font-medium mb-2 text-[var(--muted)]">
            Your Question
          </label>
          <textarea
            className="input-field mb-4"
            placeholder="e.g. How does the authentication system work? What does the login function do?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows={3}
          />
          <button
            type="submit"
            className="btn-primary flex items-center gap-2"
            disabled={loading || !question.trim()}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Thinking...
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
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
                Ask Question
              </>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="card p-4 mb-6 border-[var(--danger)]">
          <p className="text-[var(--danger)] text-sm">{error}</p>
        </div>
      )}

      {answer && (
        <div className="card p-6 mb-6">
          <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <svg
              className="w-5 h-5 text-[var(--accent)]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
            Answer
          </h2>
          <div className="text-[var(--foreground)] leading-relaxed whitespace-pre-wrap">
            {answer}
          </div>
        </div>
      )}

      {sources.length > 0 && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <svg
              className="w-5 h-5 text-[var(--muted)]"
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
            Sources
          </h2>
          <div className="space-y-2">
            {sources.map((source, i) => (
              <div key={i} className="code-block text-xs text-[var(--muted)]">
                {source}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

"use client";

import { useState } from "react";
import { explainCode } from "../lib/api";

const LANGUAGES = [
  "auto",
  "python",
  "javascript",
  "typescript",
  "java",
  "c",
  "cpp",
  "csharp",
  "go",
  "rust",
  "ruby",
  "php",
  "swift",
  "kotlin",
  "sql",
  "bash",
  "html",
  "css",
];

export default function ExplainPage() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("auto");
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleExplain(e: React.FormEvent) {
    e.preventDefault();
    if (!code.trim()) return;

    setLoading(true);
    setError("");
    setExplanation("");

    try {
      const data = await explainCode(code, language);
      setExplanation(data.explanation);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to explain code");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">
          <span className="gradient-text">AI Code</span> Explainer
        </h1>
        <p className="text-[var(--muted)]">
          Paste any code snippet and get a clear, detailed explanation powered
          by AI.
        </p>
      </div>

      <form onSubmit={handleExplain} className="mb-8">
        <div className="card p-6">
          <div className="flex items-center justify-between mb-2">
            <label className="block text-sm font-medium text-[var(--muted)]">
              Code Snippet
            </label>
            <select
              className="input-field w-auto text-sm py-1 px-3"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              {LANGUAGES.map((lang) => (
                <option key={lang} value={lang}>
                  {lang === "auto"
                    ? "Auto-detect"
                    : lang.charAt(0).toUpperCase() + lang.slice(1)}
                </option>
              ))}
            </select>
          </div>
          <textarea
            className="input-field mb-4 font-mono text-sm"
            placeholder={`Paste your code here...\n\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)`}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={10}
          />
          <button
            type="submit"
            className="btn-primary flex items-center gap-2"
            disabled={loading || !code.trim()}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
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
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                  />
                </svg>
                Explain Code
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

      {explanation && (
        <div className="card p-6">
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
            Explanation
          </h2>
          <div className="text-[var(--foreground)] leading-relaxed whitespace-pre-wrap">
            {explanation}
          </div>
        </div>
      )}
    </div>
  );
}

"use client";

import { useState, useEffect } from "react";
import { cloneAndIndex, listRepos, deleteRepo } from "../lib/api";

type RepoItem = {
  name: string;
  path: string;
};

export default function ReposPage() {
  const [repoUrl, setRepoUrl] = useState("");
  const [repos, setRepos] = useState<RepoItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [cloneStatus, setCloneStatus] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchRepos();
  }, []);

  async function fetchRepos() {
    try {
      const data = await listRepos();
      setRepos(data.repos);
    } catch {
      // Backend might not be running
    }
  }

  async function handleCloneAndIndex(e: React.FormEvent) {
    e.preventDefault();
    if (!repoUrl.trim()) return;

    setLoading(true);
    setError("");
    setCloneStatus("");

    try {
      const data = await cloneAndIndex(repoUrl);
      setCloneStatus(data.status);
      setRepoUrl("");
      fetchRepos();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to clone repository",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(repo: RepoItem) {
    if (!confirm(`Delete repository "${repo.name}"? This cannot be undone.`)) return;

    try {
      await deleteRepo(repo.name);
      fetchRepos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete");
    }
  }

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">
          <span className="gradient-text">GitHub</span> Repositories
        </h1>
        <p className="text-[var(--muted)]">
          Clone and index GitHub repositories for AI-powered code search and
          Q&A.
        </p>
      </div>

      {/* Clone Form */}
      <form onSubmit={handleCloneAndIndex} className="mb-8">
        <div className="card p-6">
          <label className="block text-sm font-medium mb-2 text-[var(--muted)]">
            GitHub Repository URL
          </label>
          <div className="flex gap-3">
            <input
              className="input-field flex-1"
              placeholder="https://github.com/user/repo  or  user/repo"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
            />
            <button
              type="submit"
              className="btn-primary flex items-center gap-2 whitespace-nowrap"
              disabled={loading || !repoUrl.trim()}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Cloning...
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
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  Clone & Index
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

      {cloneStatus && (
        <div className="card p-4 mb-6 border-[var(--success)]">
          <p className="text-[var(--success)] text-sm flex items-center gap-2">
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
                d="M5 13l4 4L19 7"
              />
            </svg>
            {cloneStatus}
          </p>
        </div>
      )}

      {/* Repository List */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
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
              d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
            />
          </svg>
          Indexed Repositories
          <span className="text-xs bg-[var(--accent)] text-white px-2 py-0.5 rounded-full ml-auto">
            {repos.length}
          </span>
        </h2>

        {repos.length === 0 ? (
          <div className="text-center py-8 text-[var(--muted)]">
            <svg
              className="w-12 h-12 mx-auto mb-3 opacity-30"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
              />
            </svg>
            <p className="text-sm">No repositories indexed yet.</p>
            <p className="text-xs mt-1">
              Clone a GitHub repo above to get started.
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {repos.map((repo) => (
              <div
                key={repo.name}
                className="flex items-center justify-between p-3 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-[var(--accent)] transition-colors"
              >
                <div className="flex items-center gap-3">
                  <svg
                    className="w-4 h-4 text-[var(--muted)]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                    />
                  </svg>
                  <span className="text-sm font-medium">{repo.name}</span>
                </div>
                <button
                  onClick={() => handleDelete(repo)}
                  className="text-[var(--muted)] hover:text-[var(--danger)] transition-colors p-1"
                  title="Delete repository"
                >
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
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

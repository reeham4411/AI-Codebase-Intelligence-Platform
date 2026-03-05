const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function askQuestion(question: string) {
  const res = await fetch(`${API_BASE}/api/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ answer: string; sources: string[] }>;
}

export async function indexRepo(data: { repo_path?: string; github_url?: string }) {
  const res = await fetch(`${API_BASE}/api/index-repo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ status: string; path: string }>;
}

export async function cloneAndIndex(repo_url: string) {
  const res = await fetch(`${API_BASE}/api/github/clone-and-index`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ status: string; local_path: string; repo_url: string }>;
}

export async function listRepos() {
  const res = await fetch(`${API_BASE}/api/github/repos`);
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ repos: string[] }>;
}

export async function deleteRepo(name: string) {
  const res = await fetch(`${API_BASE}/api/github/repos/${encodeURIComponent(name)}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function searchCode(query: string, k: number = 5) {
  const res = await fetch(`${API_BASE}/api/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, k }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{
    query: string;
    results: { content: string; source: string; score: number }[];
    total: number;
  }>;
}

export async function explainCode(code: string, language: string = "auto") {
  const res = await fetch(`${API_BASE}/api/explain`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, language }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ explanation: string; language: string }>;
}

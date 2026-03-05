"""
Index a repository into the vector database for AI search.

Usage:
    python scripts/index_repo.py <path_or_github_url>

Examples:
    python scripts/index_repo.py ../data/repos/test_repo
    python scripts/index_repo.py https://github.com/pallets/flask
    python scripts/index_repo.py pallets/flask
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

from services.rag_service import index_repo
from services.github_service import clone_github_repo


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/index_repo.py <path_or_github_url>")
        print("Examples:")
        print("  python scripts/index_repo.py ../data/repos/test_repo")
        print("  python scripts/index_repo.py pallets/flask")
        sys.exit(1)

    target = sys.argv[1]

    # If it looks like a GitHub URL or shorthand, clone it first
    if target.startswith("http") or ("/" in target and not os.path.exists(target)):
        print(f"Cloning GitHub repository: {target}")
        try:
            local_path = clone_github_repo(target)
            print(f"Cloned to: {local_path}")
        except RuntimeError as e:
            print(f"Clone error: {e}")
            sys.exit(1)
    else:
        local_path = os.path.abspath(target)

    if not os.path.exists(local_path):
        print(f"Error: Path does not exist: {local_path}")
        sys.exit(1)

    print(f"Indexing repository: {local_path}")
    index_repo(local_path)
    print("Repository indexed successfully!")


if __name__ == "__main__":
    main()

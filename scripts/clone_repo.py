"""
Clone a GitHub repository for indexing.

Usage:
    python scripts/clone_repo.py <github_url>

Examples:
    python scripts/clone_repo.py https://github.com/pallets/flask
    python scripts/clone_repo.py pallets/flask
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

from services.github_service import clone_github_repo


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/clone_repo.py <github_url>")
        print("Example: python scripts/clone_repo.py pallets/flask")
        sys.exit(1)

    repo_url = sys.argv[1]
    print(f"Cloning repository: {repo_url}")

    try:
        local_path = clone_github_repo(repo_url)
        print(f"Repository cloned to: {local_path}")
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

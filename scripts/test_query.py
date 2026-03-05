"""
Test querying the AI Codebase Assistant.

Usage:
    python scripts/test_query.py "<question>"

Examples:
    python scripts/test_query.py "how does authentication work?"
    python scripts/test_query.py "what files handle routing?"
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

from services.rag_service import answer_question


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/test_query.py "<question>"')
        print('Example: python scripts/test_query.py "how does authentication work?"')
        sys.exit(1)

    question = sys.argv[1]
    print(f"Question: {question}\n")

    answer, sources = answer_question(question)

    print(f"Answer:\n{answer}\n")
    print(f"Sources:")
    for source in sources:
        print(f"  - {source}")


if __name__ == "__main__":
    main()

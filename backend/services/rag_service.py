from transformers import pipeline

from rag.rag_pipeline import index_repository
from rag.retriever import retrieve_chunks


# local lightweight LLM (~250MB)
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=256
)


def index_repo(repo_path: str):
    """
    Index a repository into the vector database
    """
    index_repository(repo_path)


def answer_question(question: str):

    # retrieve relevant code chunks
    context_chunks, sources = retrieve_chunks(question)

    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant that helps developers understand a codebase.

Use the following code snippets to answer the question.

CODE CONTEXT:
{context_text}

QUESTION:
{question}

Explain clearly and mention relevant files if possible.
"""

    result = generator(prompt)

    answer = result[0]["generated_text"]

    return answer, list(set(sources))
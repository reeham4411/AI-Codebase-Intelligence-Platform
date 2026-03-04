import os
from langchain_openai import ChatOpenAI

from rag.rag_pipeline import index_repository
from rag.retriever import retrieve_chunks


def index_repo(repo_path: str):
    """
    Index a repository into the vector database
    """
    index_repository(repo_path)


def answer_question(question: str):

    # Retrieve relevant code chunks
    context_chunks, sources = retrieve_chunks(question)

    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant that helps developers understand a codebase.

Use the following code snippets to answer the question.

CODE CONTEXT:
{context_text}

QUESTION:
{question}

Answer clearly and reference files when possible.
"""

    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        temperature=0
    )

    response = llm.invoke(prompt)

    return response.content, list(set(sources))
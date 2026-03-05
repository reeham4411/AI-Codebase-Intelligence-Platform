import os
from groq import Groq

from rag.rag_pipeline import index_repository
from rag.retriever import retrieve_chunks


# Groq API client - free, fast, cloud-based LLM
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def index_repo(repo_path: str):
    """
    Index a repository into the vector database
    """
    index_repository(repo_path)


def answer_question(question: str):

    # retrieve relevant code chunks
    context_chunks, sources = retrieve_chunks(question)

    context_text = "\n\n".join(context_chunks)

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps developers understand a codebase. "
                       "Explain clearly and mention relevant files if possible."
        },
        {
            "role": "user",
            "content": f"Based on the following code snippets, answer my question.\n\n"
                       f"CODE CONTEXT:\n{context_text}\n\n"
                       f"QUESTION: {question}"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=512,
        temperature=0.3,
    )

    answer = response.choices[0].message.content

    return answer, list(set(sources))
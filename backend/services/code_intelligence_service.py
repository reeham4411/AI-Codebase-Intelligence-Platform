import os
from groq import Groq

from rag.retriever import retrieve_chunks

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def search_code(query: str, k: int = 5):
    """
    Intelligent code search - find relevant code snippets using semantic search.
    Returns ranked code snippets with file paths and relevance info.
    """
    context_chunks, sources = retrieve_chunks(query, k=k)

    results = []
    for chunk, source in zip(context_chunks, sources):
        results.append({
            "source": source,
            "content": chunk,
        })

    return results


def explain_code(code: str, language: str = "auto"):
    """
    Use AI to explain a piece of code in plain English.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an expert programmer. Explain code clearly and concisely. "
                       "Break down what the code does, mention any patterns or important logic, "
                       "and note potential issues or improvements."
        },
        {
            "role": "user",
            "content": f"Explain the following {language} code:\n\n```\n{code}\n```"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1024,
        temperature=0.3,
    )

    return response.choices[0].message.content

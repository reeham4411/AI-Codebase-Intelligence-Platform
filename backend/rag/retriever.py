import numpy as np

from rag.vector_store import load_vector_store
from rag.embeddings import create_embedding


def retrieve_chunks(query, k=4):

    index, metadata = load_vector_store()

    query_vector = create_embedding(query)

    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = []
    sources = []

    for i in indices[0]:

        results.append(metadata[i]["content"])
        sources.append(metadata[i]["file_path"])

    return results, sources
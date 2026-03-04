import faiss
import pickle
import numpy as np

from services.embedding_service import create_embedding

INDEX_PATH = "../data/vector_store/index.faiss"
META_PATH = "../data/vector_store/metadata.pkl"


def load_vector_store():

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def retrieve_context(question, k=3):

    index, metadata = load_vector_store()

    query_vector = create_embedding(question)

    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = []
    sources = []

    for i in indices[0]:
        results.append(metadata[i]["content"])
        sources.append(metadata[i]["file_path"])

    return results, sources
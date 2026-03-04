import os
import faiss
import pickle
import numpy as np

VECTOR_PATH = "../data/vector_store"


def save_vector_store(vectors, metadata):

    vectors = np.array(vectors).astype("float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    os.makedirs(VECTOR_PATH, exist_ok=True)

    faiss.write_index(index, f"{VECTOR_PATH}/index.faiss")

    with open(f"{VECTOR_PATH}/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)


def load_vector_store():

    index = faiss.read_index(f"{VECTOR_PATH}/index.faiss")

    with open(f"{VECTOR_PATH}/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
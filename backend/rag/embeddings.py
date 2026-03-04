from sentence_transformers import SentenceTransformer

# lightweight embedding model (~80MB)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):
    """
    Generate embedding for text using local model
    """

    embedding = embedding_model.encode(text)

    return embedding
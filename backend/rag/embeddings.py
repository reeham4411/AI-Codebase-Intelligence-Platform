import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def create_embedding(text: str):
    """
    Generate embedding for text using local model (lazy-loaded)
    """
    model = _get_model()
    embedding = model.encode(text)
    return embedding
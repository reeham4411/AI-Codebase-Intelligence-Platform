from rag.repo_loader import load_code_files
from rag.code_chunker import chunk_code
from rag.embeddings import create_embedding
from rag.vector_store import save_vector_store


def index_repository(repo_path):

    files = load_code_files(repo_path)

    vectors = []
    metadata = []

    for file in files:

        chunks = chunk_code(file["content"])

        for chunk in chunks:

            embedding = create_embedding(chunk)

            vectors.append(embedding)

            metadata.append(
                {
                    "file_path": file["file_path"],
                    "content": chunk
                }
            )

    save_vector_store(vectors, metadata)
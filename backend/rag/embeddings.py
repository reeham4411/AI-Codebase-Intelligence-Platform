import os
from langchain_openai import OpenAIEmbeddings


embedding_model = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


def create_embedding(text):

    return embedding_model.embed_query(text)
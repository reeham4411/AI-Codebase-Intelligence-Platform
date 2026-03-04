from fastapi import APIRouter
from services.rag_service import index_repository

router = APIRouter(prefix="/api", tags=["Index"])


@router.post("/index-repo")
def index_repo(repo_path: str):

    index_repository(repo_path)

    return {"status": "Repository indexed successfully"}
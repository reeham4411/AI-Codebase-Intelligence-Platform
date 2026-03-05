from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.rag_service import index_repo
from services.github_service import clone_github_repo

router = APIRouter(prefix="/api", tags=["Index"])


class IndexRequest(BaseModel):
    repo_path: Optional[str] = None
    github_url: Optional[str] = None


@router.post("/index-repo")
def index_repository(request: IndexRequest):
    """
    Index a repository. Provide either:
    - repo_path: local filesystem path
    - github_url: GitHub URL (will be cloned first)
    """
    if request.github_url:
        try:
            local_path = clone_github_repo(request.github_url)
        except RuntimeError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif request.repo_path:
        local_path = request.repo_path
    else:
        raise HTTPException(status_code=400, detail="Provide either repo_path or github_url")

    index_repo(local_path)

    return {
        "status": "Repository indexed successfully",
        "path": local_path
    }
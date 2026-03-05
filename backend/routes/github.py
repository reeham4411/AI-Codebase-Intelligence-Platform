from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.github_service import clone_github_repo, list_cloned_repos, delete_cloned_repo
from services.rag_service import index_repo

router = APIRouter(prefix="/api", tags=["GitHub"])


class GitHubRepoRequest(BaseModel):
    repo_url: str


class CloneAndIndexRequest(BaseModel):
    repo_url: str


@router.post("/github/clone")
def clone_repo(request: GitHubRepoRequest):
    """
    Clone a GitHub repository (shallow clone for speed).
    Accepts: https://github.com/user/repo or user/repo
    """
    try:
        local_path = clone_github_repo(request.repo_url)
        return {
            "status": "Repository cloned successfully",
            "local_path": local_path
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/github/clone-and-index")
def clone_and_index(request: CloneAndIndexRequest):
    """
    Clone a GitHub repository AND index it for AI search in one step.
    """
    try:
        local_path = clone_github_repo(request.repo_url)
        index_repo(local_path)
        return {
            "status": "Repository cloned and indexed successfully",
            "local_path": local_path,
            "repo_url": request.repo_url
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/github/repos")
def get_repos():
    """
    List all cloned repositories.
    """
    repos = list_cloned_repos()
    return {"repos": repos}


@router.delete("/github/repos/{repo_name}")
def remove_repo(repo_name: str):
    """
    Delete a cloned repository.
    """
    deleted = delete_cloned_repo(repo_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Repository not found")
    return {"status": f"Repository '{repo_name}' deleted"}

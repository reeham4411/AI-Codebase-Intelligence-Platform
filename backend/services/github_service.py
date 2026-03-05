import os
import subprocess
import shutil


REPO_PATH = os.getenv("REPO_PATH", "../data/repos")


def clone_github_repo(repo_url: str) -> str:
    """
    Clone a GitHub repository to the local data/repos folder.
    Accepts URLs like:
        - https://github.com/user/repo
        - https://github.com/user/repo.git
        - user/repo (shorthand)
    Returns the local path of the cloned repo.
    """

    # Handle shorthand format: user/repo -> full URL
    if not repo_url.startswith("http"):
        repo_url = f"https://github.com/{repo_url}"

    # Remove trailing .git if present for consistent folder naming
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    owner = repo_url.rstrip("/").split("/")[-2]

    local_path = os.path.abspath(os.path.join(REPO_PATH, f"{owner}__{repo_name}"))

    # If repo already exists, pull latest changes
    if os.path.exists(local_path):
        try:
            subprocess.run(
                ["git", "-C", local_path, "pull"],
                capture_output=True, text=True, check=True, timeout=120
            )
            return local_path
        except subprocess.CalledProcessError:
            # If pull fails, delete and re-clone
            shutil.rmtree(local_path, ignore_errors=True)

    os.makedirs(REPO_PATH, exist_ok=True)

    # Clone with depth=1 for speed (only latest commit)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, local_path],
        capture_output=True, text=True, timeout=300
    )

    if result.returncode != 0:
        raise RuntimeError(f"Git clone failed: {result.stderr}")

    return local_path


def list_cloned_repos() -> list:
    """
    List all currently cloned repositories.
    """
    repos_dir = os.path.abspath(REPO_PATH)

    if not os.path.exists(repos_dir):
        return []

    repos = []
    for name in os.listdir(repos_dir):
        full_path = os.path.join(repos_dir, name)
        if os.path.isdir(full_path):
            repos.append({
                "name": name,
                "path": full_path
            })

    return repos


def delete_cloned_repo(repo_name: str) -> bool:
    """
    Delete a cloned repository by name.
    """
    repo_path = os.path.abspath(os.path.join(REPO_PATH, repo_name))

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, ignore_errors=True)
        return True

    return False

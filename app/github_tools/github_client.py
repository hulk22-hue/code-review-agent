from github import Github
from urllib.parse import urlparse

def fetch_pr_files_and_diffs(repo_url, pr_number, github_token=None):
    # Parse repo_url to get owner/repo
    parts = urlparse(repo_url)
    path = parts.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    owner, repo = path.split("/")
    gh = Github(github_token) if github_token else Github()
    repo = gh.get_repo(f"{owner}/{repo}")
    pr = repo.get_pull(pr_number)
    files = []
    for f in pr.get_files():
        files.append({
            "name": f.filename,
            "patch": f.patch or "",  # The diff/patch for that file
        })
    return files
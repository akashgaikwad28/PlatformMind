class GitHubClient:
    def get_repo(self, repo_name: str) -> dict[str, str]:
        return {"name": repo_name}

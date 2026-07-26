from platformmind.infrastructure.github.client.github_client import GitHubClient


class GitHubAdapter:
    def __init__(self, client: GitHubClient):
        self.client = client

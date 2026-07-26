"""
GitHub Repository Tools.
"""

from typing import Any

from pydantic import BaseModel

from platformmind.infrastructure.github.client.client import GitHubClient
from platformmind.infrastructure.github.tools.base_tool import BaseTool


class GetRepositoryInput(BaseModel):
    # Optional overrides
    owner: str | None = None
    repo: str | None = None


class GetRepositoryTool(BaseTool[GetRepositoryInput]):
    name = "get_repository"
    description = "Gets repository metadata"
    input_schema = GetRepositoryInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: GetRepositoryInput) -> tuple[Any, int | None, int]:
        owner = inputs.owner or self.client.owner
        repo = inputs.repo or self.client.repo
        path = f"/repos/{owner}/{repo}"
        data, status = await self.client.get(path)
        return data, status, 1

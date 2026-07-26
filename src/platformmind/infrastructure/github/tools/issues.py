"""
GitHub Issue Tools.
"""

from typing import Any

from pydantic import BaseModel, Field

from platformmind.infrastructure.github.client.client import GitHubClient
from platformmind.infrastructure.github.tools.base_tool import BaseTool


class CreateIssueInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    body: str = Field(default="", max_length=65536)
    labels: list[str] = Field(default_factory=list)


class CreateIssueTool(BaseTool[CreateIssueInput]):
    name = "create_issue"
    description = "Creates a new issue on GitHub"
    input_schema = CreateIssueInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: CreateIssueInput) -> tuple[Any, int | None, int]:
        path = f"/repos/{self.client.owner}/{self.client.repo}/issues"
        payload = {"title": inputs.title, "body": inputs.body, "labels": inputs.labels}
        data, status = await self.client.post(path, json=payload)
        return data, status, 1


class UpdateIssueInput(BaseModel):
    issue_number: int
    title: str | None = Field(default=None, min_length=1, max_length=256)
    body: str | None = Field(default=None, max_length=65536)
    state: str | None = Field(default=None, pattern="^(open|closed)$")


class UpdateIssueTool(BaseTool[UpdateIssueInput]):
    name = "update_issue"
    description = "Updates an existing issue on GitHub"
    input_schema = UpdateIssueInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: UpdateIssueInput) -> tuple[Any, int | None, int]:
        path = f"/repos/{self.client.owner}/{self.client.repo}/issues/{inputs.issue_number}"
        payload = {
            k: v
            for k, v in inputs.model_dump().items()
            if v is not None and k != "issue_number"
        }
        data, status = await self.client.patch(path, json=payload)
        return data, status, 1


class CloseIssueInput(BaseModel):
    issue_number: int


class CloseIssueTool(BaseTool[CloseIssueInput]):
    name = "close_issue"
    description = "Closes an issue"
    input_schema = CloseIssueInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: CloseIssueInput) -> tuple[Any, int | None, int]:
        path = f"/repos/{self.client.owner}/{self.client.repo}/issues/{inputs.issue_number}"
        data, status = await self.client.patch(path, json={"state": "closed"})
        return data, status, 1


class SearchIssuesInput(BaseModel):
    query: str


class SearchIssuesTool(BaseTool[SearchIssuesInput]):
    name = "search_issues"
    description = "Searches issues globally or in repo"
    input_schema = SearchIssuesInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: SearchIssuesInput) -> tuple[Any, int | None, int]:
        # Scoped to current repo for safety unless overriden
        q = f"{inputs.query} repo:{self.client.owner}/{self.client.repo}"
        data, status = await self.client.get("/search/issues", params={"q": q})
        return data, status, 1

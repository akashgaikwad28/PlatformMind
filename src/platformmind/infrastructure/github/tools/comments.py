"""
GitHub Comment Tools.
"""

from typing import Any

from pydantic import BaseModel, Field

from platformmind.infrastructure.github.client.client import GitHubClient
from platformmind.infrastructure.github.tools.base_tool import BaseTool


class CreateCommentInput(BaseModel):
    issue_number: int
    body: str = Field(..., min_length=1, max_length=65536)


class CreateCommentTool(BaseTool[CreateCommentInput]):
    name = "create_comment"
    description = "Creates a comment on an issue"
    input_schema = CreateCommentInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: CreateCommentInput) -> tuple[Any, int | None, int]:
        path = f"/repos/{self.client.owner}/{self.client.repo}/issues/{inputs.issue_number}/comments"
        data, status = await self.client.post(path, json={"body": inputs.body})
        return data, status, 1

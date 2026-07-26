"""
GitHub Label Tools.
"""

from typing import Any

from pydantic import BaseModel, Field

from platformmind.infrastructure.github.client.client import GitHubClient
from platformmind.infrastructure.github.tools.base_tool import BaseTool


class AssignLabelInput(BaseModel):
    issue_number: int
    labels: list[str] = Field(..., min_length=1)


class AssignLabelTool(BaseTool[AssignLabelInput]):
    name = "assign_label"
    description = "Assigns labels to an issue"
    input_schema = AssignLabelInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: AssignLabelInput) -> tuple[Any, int | None, int]:
        path = f"/repos/{self.client.owner}/{self.client.repo}/issues/{inputs.issue_number}/labels"
        data, status = await self.client.post(path, json={"labels": inputs.labels})
        return data, status, 1


class CreateLabelInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(..., pattern="^[0-9a-fA-F]{6}$")
    description: str = Field(default="", max_length=100)


class CreateLabelTool(BaseTool[CreateLabelInput]):
    name = "create_label"
    description = "Creates a new label in the repository"
    input_schema = CreateLabelInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(self, inputs: CreateLabelInput) -> tuple[Any, int | None, int]:
        path = f"/repos/{self.client.owner}/{self.client.repo}/labels"
        payload = inputs.model_dump()
        data, status = await self.client.post(path, json=payload)
        return data, status, 1

"""
GitHub Milestone Tools.
"""

from typing import Any

from pydantic import BaseModel, Field

from platformmind.infrastructure.github.client.client import GitHubClient
from platformmind.infrastructure.github.tools.base_tool import BaseTool


class CreateMilestoneInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    state: str = Field(default="open", pattern="^(open|closed)$")
    description: str = Field(default="")


class CreateMilestoneTool(BaseTool[CreateMilestoneInput]):
    name = "create_milestone"
    description = "Creates a new milestone"
    input_schema = CreateMilestoneInput

    def __init__(self, client: GitHubClient):
        self.client = client

    async def _execute(
        self, inputs: CreateMilestoneInput
    ) -> tuple[Any, int | None, int]:
        path = f"/repos/{self.client.owner}/{self.client.repo}/milestones"
        payload = inputs.model_dump()
        data, status = await self.client.post(path, json=payload)
        return data, status, 1

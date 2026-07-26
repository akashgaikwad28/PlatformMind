"""
API Request Schemas.
"""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ExecuteRequest(BaseModel):
    """
    Request model for executing a natural language instruction.
    """

    instruction: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Natural language instruction for the autonomous agent to execute.",
        examples=[
            "Create a GitHub issue titled 'Login timeout bug' with labels 'bug' and 'high-priority'"
        ],
    )
    repository: str = Field(
        ...,
        min_length=1,
        description="Target GitHub repository context in the format 'owner/repo' or a full URL.",
        examples=[
            "https://github.com/akashgaikwad28/PlatformMind.git",
            "akashgaikwad28/PlatformMind",
        ],
    )
    options: Optional[dict[str, Any]] = Field(
        default_factory=dict,
        description="Optional execution parameters (e.g., strict_mode, max_steps).",
        examples=[{"strict_mode": True, "max_steps": 10}],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "instruction": "Find open bugs and assign them the 'triage' label",
                "repository": "akashgaikwad28/PlatformMind",
                "options": {"dry_run": False},
            }
        }
    )

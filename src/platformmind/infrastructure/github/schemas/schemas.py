"""
GitHub Tool Schemas.
"""

from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """Standardized result wrapper for all tools."""

    success: bool
    tool_name: str
    execution_time: float
    api_calls: int
    status_code: int | None = None
    data: dict[str, Any] | list[Any] | None = None
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

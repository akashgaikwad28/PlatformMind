"""
Memory Domain Models.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from platformmind.core.utils.clock import Clock
from platformmind.domain.enums import MemoryCategory
from platformmind.domain.models.constraint import Constraint
from platformmind.domain.value_objects import ExecutionId, MemoryId


class MemoryEntry(BaseModel):
    """
    Represents a generic memory object.
    """

    id: MemoryId = Field(default_factory=MemoryId)
    category: MemoryCategory
    content: dict[str, Any]
    embedding_id: str | None = None
    confidence: float = Field(default=1.0)
    created_at: datetime = Field(default_factory=Clock.now)

    model_config = ConfigDict(frozen=True)


class ExecutionRecord(BaseModel):
    """
    Represents stored execution memory.
    """

    execution_id: ExecutionId
    instruction: str
    execution_summary: str
    metrics: dict[str, Any] = Field(default_factory=dict)
    constraints: list[Constraint] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=Clock.now)

    model_config = ConfigDict(frozen=True)

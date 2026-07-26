from typing import Any

"""
Memory Engine Schemas / DTOs.
"""

from pydantic import BaseModel, ConfigDict

from platformmind.domain.models.capability import Capability
from platformmind.domain.models.constraint import Constraint
from platformmind.domain.models.memory import ExecutionRecord


class RankedMemory(BaseModel):
    model_config = ConfigDict(frozen=True)
    item: ExecutionRecord | Capability | Constraint | dict
    type: str  # "execution", "capability", "constraint"
    similarity: float = 0.0
    recency_score: float = 0.0
    success_rate: float = 0.0
    confidence: float = 0.0
    final_score: float = 0.0


class MemoryContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    executions: list[RankedMemory] = []
    capabilities: list[RankedMemory] = []
    constraints: list[RankedMemory] = []
    summary: str = ""
    metrics: dict[str, Any] = {}


class CompactionReport(BaseModel):
    model_config = ConfigDict(frozen=True)
    archived_count: int
    summarized_count: int
    freed_bytes: int = 0

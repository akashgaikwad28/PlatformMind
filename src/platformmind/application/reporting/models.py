"""
Unified Report Domain Model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ExecutionReport:
    """
    Unified summary of the entire execution.
    """

    execution_id: str
    instruction: str
    timestamp: datetime
    status: str
    timeline: list[str]
    planner: dict[str, Any]
    execution: dict[str, Any]
    metrics: dict[str, Any]
    learning: dict[str, Any]
    memory: dict[str, Any]
    synthesis: dict[str, Any]
    memory_before: dict[str, Any] = None
    memory_after: dict[str, Any] = None
    memory_delta: dict[str, Any] = None

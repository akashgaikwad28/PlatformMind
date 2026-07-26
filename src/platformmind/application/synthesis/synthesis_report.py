"""
Synthesis Report.
"""

from dataclasses import dataclass
from typing import Any

from platformmind.domain.models.execution import ExecutionPlan


@dataclass
class SynthesisReport:
    """
    Structured output of the synthesis process.
    """

    success: bool
    instruction: str
    missing_workflow: bool
    capability_id: str | None = None
    design: dict[str, Any] | None = None
    plan: ExecutionPlan | None = None
    errors: list[str] | None = None

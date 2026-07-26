"""
Knowledge Extractor Component.
"""

import uuid

from platformmind.core.utils.clock import Clock
from platformmind.domain.enums import ConstraintSeverity, ConstraintType
from platformmind.domain.models.capability import Capability
from platformmind.domain.models.constraint import Constraint
from platformmind.domain.models.memory import ExecutionRecord
from platformmind.domain.value_objects import CapabilityId


class KnowledgeExtractor:
    """
    Analyzes ExecutionResults to isolate Constraints, new Capabilities, and performance metrics.
    """

    def extract_constraints(self, record: ExecutionRecord) -> list[Constraint]:
        constraints = []
        metrics = record.metrics or {}

        # Example logic for constraint extraction from raw logs/warnings
        # In a real system, this would use LLM analysis
        warnings = metrics.get("warnings", [])
        for w in warnings:
            if "permission denied" in str(w).lower():
                constraints.append(
                    Constraint(
                        id=str(uuid.uuid4()),
                        type=ConstraintType.PERMISSION_DENIED,
                        description=str(w),
                        severity=ConstraintSeverity.ERROR,
                        discovered_at=Clock.now(),
                    )
                )
            elif "rate limit" in str(w).lower():
                constraints.append(
                    Constraint(
                        id=str(uuid.uuid4()),
                        type=ConstraintType.RATE_LIMIT,
                        description=str(w),
                        severity=ConstraintSeverity.CRITICAL,
                        discovered_at=Clock.now(),
                    )
                )

        failures = metrics.get("failures", [])
        for f in failures:
            constraints.append(
                Constraint(
                    id=str(uuid.uuid4()),
                    type=ConstraintType.BUSINESS_RULE,
                    description=str(f),
                    severity=ConstraintSeverity.ERROR,
                    discovered_at=Clock.now(),
                )
            )

        return constraints

    def extract_capability(self, record: ExecutionRecord) -> Capability | None:
        """
        Determines if an execution record represents a reusable capability.
        """
        metrics = record.metrics or {}
        if not metrics.get("failures") and metrics.get("success", False):
            # If completely successful, might be worth registering as a basic capability
            return Capability(
                id=CapabilityId(value=str(uuid.uuid4())),
                name=f"GeneratedCapability_{str(uuid.uuid4())[:8]}",
                description=record.instruction,
                execution_strategy={"summary": record.execution_summary},
                average_execution_time=metrics.get("execution_time", 0.0),
                created_at=Clock.now(),
            )
        return None

"""
Capability Matcher.
"""

from typing import Any

from pydantic import BaseModel, Field

from platformmind.domain.models.planning_context import PlanningContext


class CapabilityMatch(BaseModel):
    """
    Rich explanation of why a capability matched a task.
    """

    capability_name: str
    score: float
    reason: str
    success_rate: float = 1.0
    constraints: list[str] = Field(default_factory=list)


class CapabilityMatcher:
    def match(
        self, tasks: list[dict[str, Any]], context: PlanningContext
    ) -> dict[str, CapabilityMatch]:
        """
        Matches tasks to existing capability memory.
        Returns a mapping of task_id -> CapabilityMatch
        """
        matches = {}
        cap_memory = context.capability_memory
        if not cap_memory:
            return matches

        # Combine known and synthesized capabilities
        all_caps = cap_memory.known_capabilities + cap_memory.synthesized_capabilities

        for task in tasks:
            desc = task.get("description", "").lower()
            name = task.get("name", "").lower()

            best_match = None
            best_score = 0.0

            for cap_name in all_caps:
                score = 0.0

                # Simple keyword matching for MVP scoring
                if (
                    cap_name.replace("_", " ") in desc
                    or cap_name.replace("_", " ") in name
                ):
                    score += 0.6
                elif any(word in desc for word in cap_name.split("_")):
                    score += 0.3

                success_rate = cap_memory.success_rates.get(cap_name, 1.0)
                score += success_rate * 0.4

                if score > best_score:
                    best_score = score
                    best_match = cap_name

            if best_match and best_score > 0.4:
                matches[task["id"]] = CapabilityMatch(
                    capability_name=best_match,
                    score=round(best_score, 2),
                    reason=f"Matched keywords with score {round(best_score, 2)} and historical success {cap_memory.success_rates.get(best_match, 1.0)}",
                    success_rate=cap_memory.success_rates.get(best_match, 1.0),
                    constraints=[],
                )

        return matches

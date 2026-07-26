"""
Confidence Estimator.
"""

from typing import Any


class ConfidenceEstimator:
    """
    Calculates overall planner confidence based on intent, memory, capabilities, and tool matching.
    """

    def estimate(
        self,
        intent_confidence: float,
        memory_context: list[dict[str, Any]],
        capability_matches: dict[str, Any],
        tasks: list[dict[str, Any]],
        tool_selection: dict[str, str],
    ) -> float:
        score = intent_confidence * 0.4

        # Penalize for missing tool mappings
        unmapped_tools = sum(
            1
            for t in tool_selection.values()
            if (t.tool if hasattr(t, "tool") else str(t)) in ("unknown_tool", "unknown")
        )
        if len(tasks) > 0:
            tool_score = 1.0 - (unmapped_tools / len(tasks))
            score += tool_score * 0.3
        else:
            score += 0.3

        # Boost for capability matches
        if capability_matches and len(tasks) > 0:
            cap_score = len(capability_matches) / len(tasks)
            score += cap_score * 0.2
        else:
            score += 0.1  # Base score if no capabilities exist

        # Consider memory constraints (just a placeholder logic)
        score += 0.1

        # Clamp between 0.0 and 1.0
        return max(0.0, min(1.0, score))

"""
Risk Analyzer.
"""

from typing import Any

from platformmind.application.planner.validators.guardrails import PolicyEngine
from platformmind.domain.models.planning_context import PlanningContext


class RiskAnalyzer:
    """
    Analyzes execution plan for potential risks and constraint violations.
    """

    def analyze(self, tasks: list[dict[str, Any]], context: PlanningContext) -> float:
        """
        Calculates a risk score between 0.0 and 1.0 based on the tools selected
        and the potential blast radius.
        """
        if not tasks:
            return 0.0

        total_risk = 0.0
        high_risk_count = 0
        mutation_count = 0

        for task in tasks:
            tool_name = task.get("tool", "")

            # Immediately cap risk if a forbidden tool is somehow planned
            if not PolicyEngine.is_tool_allowed(tool_name):
                return 1.0

            if PolicyEngine.is_high_risk(tool_name):
                high_risk_count += 1
                total_risk += 0.5

            # Basic heuristics for mutation blast radius
            if any(
                verb in tool_name
                for verb in ["create", "update", "close", "assign", "add", "remove"]
            ):
                mutation_count += 1
                total_risk += 0.1

        # Adjust for blast radius (e.g. attempting >10 mutations at once is inherently risky)
        if mutation_count > 10:
            total_risk += 0.3

        return min(total_risk, 1.0)

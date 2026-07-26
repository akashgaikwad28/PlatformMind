"""
Tool Profiler.
"""

from typing import Any

from platformmind.application.learning.score_manager import ScoreManager


class ToolProfiler:
    """
    Maintains statistics for every tool.
    """

    def __init__(self, score_manager: ScoreManager):
        self.score_manager = score_manager

    def update_tool_stats(
        self, historical_stats: dict[str, Any], current_success: bool
    ) -> dict[str, Any]:
        """
        Updates the success rate of a tool based on the current execution.
        """
        historical_rate = historical_stats.get("success_rate", 1.0)
        new_rate = 1.0 if current_success else 0.0

        updated_rate = self.score_manager.update_score(historical_rate, new_rate)

        return {
            "usage_count": historical_stats.get("usage_count", 0) + 1,
            "success_rate": updated_rate,
        }

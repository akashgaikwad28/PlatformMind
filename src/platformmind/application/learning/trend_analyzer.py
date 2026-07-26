"""
Trend Analyzer.
"""

from typing import Any


class TrendAnalyzer:
    """
    Analyzes historical trends for degrading performance or increasing capability adoption.
    """

    def analyze_trends(self, run_history: list[dict[str, Any]]) -> list[str]:
        trends = []
        if not run_history or len(run_history) < 2:
            return ["Insufficient data for trend analysis."]

        first = run_history[0]
        last = run_history[-1]

        # Check execution time
        if last.get("total_time", 0) < first.get("total_time", 0):
            trends.append("Execution time is decreasing.")
        else:
            trends.append("Execution time is increasing or stagnant.")

        # Check retries
        if last.get("total_retries", 0) < first.get("total_retries", 0):
            trends.append("Retry count is decreasing, system is stabilizing.")

        return trends

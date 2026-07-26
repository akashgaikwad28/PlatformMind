"""
Metrics Collector.
"""

from typing import Any


class MetricsCollector:
    """
    Aggregates metrics for the learning session.
    """

    def collect(self, facts: dict[str, Any]) -> dict[str, Any]:
        return {
            "total_time": facts.get("execution_time", 0.0),
            "total_calls": facts.get("api_calls", 0),
            "total_retries": facts.get("retries", 0),
            "success": facts.get("status") == "COMPLETED",
        }

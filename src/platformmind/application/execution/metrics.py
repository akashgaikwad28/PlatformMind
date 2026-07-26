"""
Metrics Tracker.
"""

from dataclasses import dataclass


@dataclass
class ExecutionMetrics:
    total_duration_seconds: float = 0.0
    api_calls: int = 0
    total_retries: int = 0
    steps_succeeded: int = 0
    steps_failed: int = 0
    steps_skipped: int = 0
    rollbacks_attempted: int = 0
    rollbacks_failed: int = 0

    def add_api_calls(self, count: int) -> None:
        self.api_calls += count

    def add_retry(self) -> None:
        self.total_retries += 1

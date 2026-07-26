"""
Report Storage.
"""

from typing import Optional

from platformmind.application.reporting.models import ExecutionReport


class ReportStore:
    """
    Persists and retrieves ExecutionReports.
    """

    def __init__(self):
        self._store = {}

    def save(self, report: ExecutionReport):
        self._store[report.execution_id] = report

    def get(self, execution_id: str) -> Optional[ExecutionReport]:
        return self._store.get(execution_id)

    def get_all(self) -> list[ExecutionReport]:
        return list(self._store.values())

"""
Report Search.
"""

from platformmind.application.reporting.models import ExecutionReport
from platformmind.application.reporting.storage import ReportStore


class ReportSearcher:
    """
    Searches stored reports.
    """

    def __init__(self, store: ReportStore):
        self.store = store

    def search_by_instruction(self, keyword: str) -> list[ExecutionReport]:
        results = []
        for report in self.store.get_all():
            if keyword.lower() in report.instruction.lower():
                results.append(report)
        return results

    def search_by_status(self, status: str) -> list[ExecutionReport]:
        return [r for r in self.store.get_all() if r.status == status]

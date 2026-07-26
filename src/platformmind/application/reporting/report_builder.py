"""
Report Builder.
"""

from datetime import datetime

from platformmind.application.reporting.models import ExecutionReport


class ReportBuilder:
    """
    Builds the unified report.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self._execution_id = "unknown"
        self._instruction = "unknown"
        self._status = "UNKNOWN"
        self._timeline = []
        self._planner = {}
        self._execution = {}
        self._metrics = {}
        self._learning = {}
        self._memory = {}
        self._synthesis = {}
        self._memory_before = {}
        self._memory_after = {}
        self._memory_delta = {}

    def set_execution_info(self, execution_id: str, instruction: str, status: str):
        self._execution_id = execution_id
        self._instruction = instruction
        self._status = status

    def add_planner_data(self, data: dict):
        self._planner.update(data)

    def add_execution_data(self, data: dict):
        self._execution.update(data)

    def add_metrics_data(self, data: dict):
        self._metrics.update(data)

    def add_learning_data(self, data: dict):
        self._learning.update(data)

    def add_memory_data(self, data: dict):
        self._memory.update(data)

    def set_memory_snapshots(
        self, memory_before: dict, memory_after: dict, memory_delta: dict
    ):
        self._memory_before = memory_before or {}
        self._memory_after = memory_after or {}
        self._memory_delta = memory_delta or {}

    def add_synthesis_data(self, data: dict):
        self._synthesis.update(data)

    def set_timeline(self, timeline: list[str]):
        self._timeline = timeline

    def build(self) -> ExecutionReport:
        return ExecutionReport(
            execution_id=self._execution_id,
            instruction=self._instruction,
            timestamp=datetime.now(),
            status=self._status,
            timeline=self._timeline,
            planner=self._planner,
            execution=self._execution,
            metrics=self._metrics,
            learning=self._learning,
            memory=self._memory,
            synthesis=self._synthesis,
            memory_before=self._memory_before,
            memory_after=self._memory_after,
            memory_delta=self._memory_delta,
        )

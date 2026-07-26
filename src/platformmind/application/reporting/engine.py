"""
Reporting Engine Facade.
"""

from platformmind.application.reporting.models import ExecutionReport
from platformmind.application.reporting.report_builder import ReportBuilder
from platformmind.application.reporting.reporters import (
    ExecutionReporter,
    LearningReporter,
    MemoryReporter,
    MetricsReporter,
    PlannerReporter,
    SynthesisReporter,
)
from platformmind.application.reporting.storage import ReportStore


class ReportingEngineImpl:
    """
    Coordinates building, exporting, and saving reports.
    """

    def __init__(self, store: ReportStore):
        self.store = store
        self.builder = ReportBuilder()
        self.execution_reporter = ExecutionReporter()
        self.planner_reporter = PlannerReporter()
        self.metrics_reporter = MetricsReporter()
        self.learning_reporter = LearningReporter()
        self.synthesis_reporter = SynthesisReporter()
        self.memory_reporter = MemoryReporter()

    def generate_report(
        self,
        instruction: str,
        plan,
        result,
        learning_report,
        synthesis_report,
        memory_stats,
        memory_before: dict = None,
        memory_after: dict = None,
        memory_delta: dict = None,
    ) -> ExecutionReport:
        self.builder.reset()

        self.builder.set_execution_info(
            result.execution_id.value, instruction, result.status.value
        )
        self.planner_reporter.report(self.builder, plan)
        self.execution_reporter.report(self.builder, result)
        self.metrics_reporter.report(self.builder, result)

        if learning_report:
            self.learning_reporter.report(self.builder, learning_report)
        if synthesis_report:
            self.synthesis_reporter.report(self.builder, synthesis_report)
        if memory_stats:
            self.memory_reporter.report(self.builder, memory_stats)

        self.builder.set_memory_snapshots(memory_before, memory_after, memory_delta)

        report = self.builder.build()
        self.store.save(report)
        return report

    def get_reports(self) -> list[ExecutionReport]:
        if hasattr(self.store, "get_all"):
            return self.store.get_all()
        if hasattr(self.store, "get_all_reports"):
            return self.store.get_all_reports()
        return []

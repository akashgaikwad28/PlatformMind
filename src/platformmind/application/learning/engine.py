"""
Learning Engine Facade.
"""

from platformmind.application.learning.analyzer import ExecutionAnalyzer
from platformmind.application.learning.improvement_calculator import (
    ImprovementCalculator,
)
from platformmind.application.learning.metrics_collector import MetricsCollector
from platformmind.application.learning.reports import LearningReport
from platformmind.application.learning.tool_profiler import ToolProfiler
from platformmind.application.learning.trend_analyzer import TrendAnalyzer
from platformmind.application.memory.services.learning import LearningMemoryService
from platformmind.domain.models.execution import ExecutionResult


class LearningEngineImpl:
    """
    Primary orchestrator for the learning pipeline.
    """

    def __init__(
        self,
        analyzer: ExecutionAnalyzer,
        metrics_collector: MetricsCollector,
        tool_profiler: ToolProfiler,
        improvement_calc: ImprovementCalculator,
        trend_analyzer: TrendAnalyzer,
        learning_service: LearningMemoryService,
    ):
        self.analyzer = analyzer
        self.metrics_collector = metrics_collector
        self.tool_profiler = tool_profiler
        self.improvement_calc = improvement_calc
        self.trend_analyzer = trend_analyzer
        self.learning_service = learning_service

    async def learn_from_execution(self, result: ExecutionResult) -> LearningReport:
        # 1. Analyze raw facts
        facts = self.analyzer.analyze(result)

        # 2. Extract Metrics
        current_metrics = self.metrics_collector.collect(facts)

        # 3. Fetch Historical Data from DB
        historical_metrics = await self.learning_service.get_historical_metrics()

        # 4. Calculate Improvements (Run N vs Run 1)
        improvements = {
            "time_improvement_pct": self.improvement_calc.calculate_improvement(
                historical_metrics.get("total_time", 0.0),
                current_metrics["total_time"],
                invert=True,
            ),
            "calls_improvement_pct": self.improvement_calc.calculate_improvement(
                historical_metrics.get("total_calls", 0),
                current_metrics["total_calls"],
                invert=True,
            ),
            "retries_improvement_pct": self.improvement_calc.calculate_improvement(
                historical_metrics.get("total_retries", 0),
                current_metrics["total_retries"],
                invert=True,
            ),
        }

        # 5. Analyze Trends
        # In a fully fleshed out trend analyzer, we'd fetch the full history, but we'll mock the list wrapping for now
        run_history = [historical_metrics, current_metrics]
        trends = self.trend_analyzer.analyze_trends(run_history)

        # 5. Generate Recommendations
        recs = []
        if improvements["retries_improvement_pct"] > 0:
            recs.append("Retries reduced! Continue using current capability mapping.")

        # 6. Build Report
        report = LearningReport(
            execution_id=facts["execution_id"],
            current_metrics=current_metrics,
            historical_averages=historical_metrics,
            improvements=improvements,
            trends=trends,
            recommendations=recs,
        )

        # Persist the current execution metrics to the DB
        await self.learning_service.save_metrics(
            {
                "execution_id": facts["execution_id"],
                "status": facts.get("status", "SUCCESS"),
                "total_time": current_metrics["total_time"],
                "total_calls": current_metrics["total_calls"],
            }
        )

        return report

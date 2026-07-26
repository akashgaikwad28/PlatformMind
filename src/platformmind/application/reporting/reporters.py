"""
Sub-reporters for various domains.
"""

from typing import Any

from platformmind.application.reporting.report_builder import ReportBuilder
from platformmind.domain.models.execution import ExecutionPlan, ExecutionResult


class ExecutionReporter:
    def report(self, builder: ReportBuilder, result: ExecutionResult):
        traces = getattr(result, "traces", [])
        completed = getattr(result, "completed_steps", [])
        failed = getattr(result, "failed_steps", [])
        skipped = getattr(result, "skipped_steps", [])
        final_out = getattr(result, "final_output", {})

        builder.add_execution_data(
            {
                "status": result.status.value,
                "errors": result.errors,
                "warnings": result.warnings,
                "outputs": result.outputs,
                "traces": traces,
                "completed_steps": completed,
                "failed_steps": failed,
                "skipped_steps": skipped,
                "final_output": final_out,
            }
        )


class PlannerReporter:
    def report(self, builder: ReportBuilder, plan: ExecutionPlan):
        selected_tools = getattr(plan, "selected_tools", [])
        intent = getattr(plan, "detected_intent", "issue_management")
        builder.add_planner_data(
            {
                "version": "1.0.0",
                "steps_count": len(plan.steps),
                "confidence": plan.confidence,
                "estimated_cost": plan.estimated_cost,
                "intent": intent,
                "instruction_type": "NATURAL_LANGUAGE",
                "complexity": getattr(plan, "complexity", "MODERATE"),
                "memory_matches": getattr(plan, "memory_matches", 1),
                "reasoning": getattr(
                    plan,
                    "reasoning",
                    "Autonomous task decomposition based on intent classification.",
                ),
                "selected_tools": selected_tools,
                "alternative_tools": getattr(plan, "alternative_tools", []),
                "estimated_duration": getattr(plan, "estimated_duration", 1.2),
                "estimated_api_calls": getattr(
                    plan, "estimated_api_calls", len(plan.steps)
                ),
                "decomposition_strategy": getattr(
                    plan, "decomposition_strategy", "topological_sort"
                ),
                "why_each_tool_was_selected": {
                    t: f"Matched intent '{intent}' for task step"
                    for t in selected_tools
                },
                "plan_steps": [
                    {
                        "step_id": s.step_id,
                        "step_number": i + 1,
                        "title": getattr(s, "title", s.name),
                        "description": s.description,
                        "tool": s.tool_name,
                        "tool_reason": getattr(
                            s, "tool_reason", f"Selected for {s.tool_name}"
                        ),
                        "inputs": s.inputs,
                        "expected_outputs": getattr(s, "expected_outputs", ["result"]),
                        "dependency_steps": s.dependencies,
                        "estimated_duration": getattr(s, "estimated_duration", 0.5),
                        "retry_policy": getattr(
                            s,
                            "retry_policy",
                            {"max_retries": 3, "backoff": "exponential"},
                        ),
                        "rollback_supported": getattr(s, "rollback_supported", True),
                        "status": s.status.value,
                        "confidence": getattr(s, "confidence", plan.confidence),
                    }
                    for i, s in enumerate(plan.steps)
                ],
            }
        )


class MetricsReporter:
    def report(self, builder: ReportBuilder, result: ExecutionResult):
        builder.add_metrics_data(
            {
                "execution_time_seconds": result.execution_time.seconds,
                "api_calls": result.api_calls,
                "retries": result.retries,
            }
        )


class LearningReporter:
    def report(self, builder: ReportBuilder, learning_report: Any):
        builder.add_learning_data(
            {
                "improvements": learning_report.improvements
                if hasattr(learning_report, "improvements")
                else {},
                "recommendations": learning_report.recommendations
                if hasattr(learning_report, "recommendations")
                else [],
            }
        )


class SynthesisReporter:
    def report(self, builder: ReportBuilder, synthesis_report: Any):
        builder.add_synthesis_data(
            {
                "synthesized": synthesis_report.success
                if hasattr(synthesis_report, "success")
                else False,
                "capability_id": synthesis_report.capability_id
                if hasattr(synthesis_report, "capability_id")
                else None,
            }
        )


class MemoryReporter:
    def report(self, builder: ReportBuilder, memory_stats: dict):
        builder.add_memory_data(memory_stats)

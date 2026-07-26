"""
Execution Orchestrator.
"""

from typing import Any

from platformmind.application.execution.execution_context import ExecutionContext
from platformmind.application.execution.executor import StepExecutor
from platformmind.application.execution.metrics import ExecutionMetrics
from platformmind.application.execution.result_builder import ExecutionResultBuilder
from platformmind.application.execution.retry import RetryManager
from platformmind.application.execution.rollback import RollbackManager
from platformmind.application.execution.state_manager import ExecutionStateManager
from platformmind.core.telemetry.tracer import trace_step
from platformmind.core.utils.clock import Clock
from platformmind.domain.models.execution import ExecutionPlan, ExecutionResult
from platformmind.infrastructure.github.schemas.schemas import ToolResult
from platformmind.infrastructure.logging.logger import get_logger

logger = get_logger()


class ExecutionOrchestrator:
    """
    Coordinates the execution of an ExecutionPlan.
    """

    def __init__(
        self,
        step_executor: StepExecutor,
        retry_manager: RetryManager,
        rollback_manager: RollbackManager,
        result_builder: ExecutionResultBuilder,
    ):
        self.step_executor = step_executor
        self.retry_manager = retry_manager
        self.rollback_manager = rollback_manager
        self.result_builder = result_builder

    def _resolve_inputs(self, inputs: dict, outputs: dict) -> dict:
        """Resolves task references, placeholders, and schema drift."""
        # Handle common LLM single vs plural typo for labels
        if "label" in inputs and "labels" not in inputs:
            lbl = inputs.pop("label")
            inputs["labels"] = [lbl] if isinstance(lbl, str) else lbl

        # Normalize hex color codes (strip leading # for GitHub API)
        if "color" in inputs and isinstance(inputs["color"], str):
            inputs["color"] = inputs["color"].lstrip("#")

        resolved = {}
        for k, v in inputs.items():
            is_ref = isinstance(v, str) and v.startswith("@")
            is_placeholder = isinstance(v, str) and (
                v in ("variable", "issue_number", "id")
                or "{{" in v
                or "<" in v
                or (k == "issue_number" and not v.isdigit())
            )

            if is_ref:
                ref = v[1:]
                if ref in outputs:
                    data = outputs[ref]
                    resolved[k] = self._extract_value_for_key(k, data)
                else:
                    resolved[k] = self._fallback_extract_for_key(k, outputs, default=v)
            elif is_placeholder:
                resolved[k] = self._fallback_extract_for_key(k, outputs, default=v)
            else:
                resolved[k] = v

        if not resolved.get("query"):
            resolved["query"] = "is:open is:issue"

        return resolved

    def _extract_value_for_key(self, key: str, data: Any) -> Any:
        if key == "issue_number":
            if isinstance(data, dict):
                if (
                    "items" in data
                    and isinstance(data["items"], list)
                    and data["items"]
                ):
                    return data["items"][0].get("number")
                if "number" in data:
                    return data["number"]
        return data

    def _fallback_extract_for_key(self, key: str, outputs: dict, default: Any) -> Any:
        for step_id in reversed(list(outputs.keys())):
            data = outputs[step_id]
            val = self._extract_value_for_key(key, data)
            if val is not data and val is not None:
                return val
        return default

    @trace_step("ExecutionOrchestrator.execute")
    async def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        state = ExecutionStateManager()
        metrics = ExecutionMetrics()
        context = ExecutionContext(execution_id=plan.plan_id.value, plan=plan)

        state.start_execution()
        start_time = Clock.now()
        outputs = {}
        errors = []
        traces = []
        completed_steps = []
        failed_steps = []
        skipped_steps = []

        try:
            # We assume tasks are already topologically sorted by the planner
            for i, step in enumerate(plan.steps):
                step_start = Clock.now()
                state.start_step(step.step_id)
                step.inputs = self._resolve_inputs(step.inputs, outputs)
                logger.info(
                    f"Executing step {step.step_id}: {step.name} (tool={step.tool_name}, inputs={step.inputs})"
                )

                # Execute with retry logic for arbitrary exceptions from the executor
                try:
                    result: ToolResult = await self.retry_manager.execute_with_retry(
                        action=lambda: self.step_executor.execute(step),
                        is_retryable=lambda e: True,
                    )
                except Exception as e:
                    step_end = Clock.now()
                    duration = (step_end - step_start).total_seconds()
                    logger.error(f"Step {step.step_id} failed permanently: {e}")
                    err_msg = f"Step {step.step_id} failed permanently: {str(e)}"
                    errors.append(err_msg)
                    state.fail_step(step.step_id)
                    failed_steps.append(step.step_id)
                    metrics.steps_failed += 1

                    traces.append(
                        {
                            "step_id": step.step_id,
                            "step_number": i + 1,
                            "title": getattr(step, "title", step.name),
                            "description": step.description,
                            "tool": step.tool_name,
                            "request": step.inputs,
                            "response": {"error": str(e)},
                            "status": "FAILED",
                            "duration": round(duration, 2),
                            "retry_count": 3,
                            "warnings": [],
                            "errors": [err_msg],
                            "api_calls": 0,
                            "started_at": step_start.isoformat(),
                            "finished_at": step_end.isoformat(),
                            "execution_order": i + 1,
                        }
                    )

                    # Mark remaining steps as skipped
                    skipped_steps = [s.step_id for s in plan.steps[i + 1 :]]
                    raise RuntimeError("Execution failed") from e

                step_end = Clock.now()
                duration = (step_end - step_start).total_seconds()
                metrics.add_api_calls(result.api_calls)

                if not result.success:
                    logger.error(
                        f"Step {step.step_id} tool returned failure: {result.errors}"
                    )
                    errors.extend(result.errors)
                    state.fail_step(step.step_id)
                    failed_steps.append(step.step_id)
                    metrics.steps_failed += 1

                    traces.append(
                        {
                            "step_id": step.step_id,
                            "step_number": i + 1,
                            "title": getattr(step, "title", step.name),
                            "description": step.description,
                            "tool": step.tool_name,
                            "request": step.inputs,
                            "response": {"errors": result.errors},
                            "status": "FAILED",
                            "duration": round(duration, 2),
                            "retry_count": 1,
                            "warnings": getattr(result, "warnings", []),
                            "errors": result.errors,
                            "api_calls": getattr(result, "api_calls", 1),
                            "started_at": step_start.isoformat(),
                            "finished_at": step_end.isoformat(),
                            "execution_order": i + 1,
                        }
                    )

                    skipped_steps = [s.step_id for s in plan.steps[i + 1 :]]
                    raise RuntimeError(f"Step {step.step_id} failed: {result.errors}")

                # Success
                outputs[step.step_id] = result.data
                state.complete_step(step.step_id)
                completed_steps.append(step.step_id)
                metrics.steps_succeeded += 1

                traces.append(
                    {
                        "step_id": step.step_id,
                        "step_number": i + 1,
                        "title": getattr(step, "title", step.name),
                        "description": step.description,
                        "tool": step.tool_name,
                        "request": step.inputs,
                        "response": result.data
                        if isinstance(result.data, dict)
                        else {"output": result.data},
                        "status": "SUCCESS",
                        "duration": round(duration, 2),
                        "retry_count": 0,
                        "warnings": getattr(result, "warnings", []),
                        "errors": [],
                        "api_calls": getattr(result, "api_calls", 1),
                        "started_at": step_start.isoformat(),
                        "finished_at": step_end.isoformat(),
                        "execution_order": i + 1,
                    }
                )

            state.complete_execution()

        except RuntimeError:
            state.fail_execution()
            logger.warning("Execution failed, attempting rollback...")
            rollback_success = await self.rollback_manager.rollback()
            if rollback_success:
                state.rollback_execution()

        finally:
            metrics.total_duration_seconds = (Clock.now() - start_time).total_seconds()

        # Build natural language answer & structured result
        final_output = self._build_final_output(
            plan, outputs, errors, completed_steps, failed_steps
        )

        return self.result_builder.build(
            execution_id=plan.plan_id.value,
            state=state,
            metrics=metrics,
            outputs=outputs,
            errors=errors,
            traces=traces,
            completed_steps=completed_steps,
            failed_steps=failed_steps,
            skipped_steps=skipped_steps,
            final_output=final_output,
        )

    def _build_final_output(
        self,
        plan: ExecutionPlan,
        outputs: dict,
        errors: list[str],
        completed: list[str],
        failed: list[str],
    ) -> dict:
        instruction = getattr(plan, "instruction_text", "Instruction")
        if failed:
            return {
                "answer": f"Execution encountered a failure during step execution: {errors[0] if errors else 'Tool failure'}.",
                "structured_result": {
                    "completed_steps": completed,
                    "failed_steps": failed,
                    "errors": errors,
                },
                "summary": f"Failed to complete instruction '{instruction}' due to errors.",
            }

        # Inspect outputs for search results or issue objects
        items_count = 0
        repo_name = "target repository"
        query_used = ""
        for data in outputs.values():
            if isinstance(data, dict):
                if "items" in data and isinstance(data["items"], list):
                    items_count += len(data["items"])
                elif "total_count" in data and isinstance(data["total_count"], int):
                    items_count = data["total_count"]
                if "query" in data:
                    query_used = data["query"]

        if items_count > 0 or query_used:
            answer = f"Found {items_count} open issue(s) in {repo_name} matching query '{query_used or 'open issues'}'."
            structured = {
                "issue_count": items_count,
                "repository": repo_name,
                "query": query_used or "is:open",
                "completed_steps": len(completed),
            }
        else:
            answer = f"Successfully executed all {len(completed)} planned step(s) for instruction: '{instruction}'."
            structured = {
                "steps_completed": len(completed),
                "tools_used": getattr(plan, "selected_tools", []),
                "outputs_summary": {k: "success" for k in outputs.keys()},
            }

        return {
            "answer": answer,
            "structured_result": structured,
            "summary": f"Instruction '{instruction}' was executed successfully.",
        }

from typing import Any

from platformmind.application.execution.orchestrator import ExecutionOrchestrator
from platformmind.application.planner.pipeline import PlanningPipeline
from platformmind.domain.models.execution import ExecutionResult
from platformmind.domain.models.instruction import Instruction


class PlatformAgent:
    """
    Autonomous ReAct Loop Agent.
    Coordinates the Planner and Orchestrator to support dynamic replanning.
    """

    def __init__(self, planner: PlanningPipeline, orchestrator: ExecutionOrchestrator):
        self.planner = planner
        self.orchestrator = orchestrator

    async def execute(
        self, instruction_text: str, repository: str, options: dict[str, Any]
    ) -> ExecutionResult:
        instruction = Instruction(original_text=instruction_text)

        previous_results = []
        final_result = None
        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Step 1: Plan
            plan = await self.planner.execute(
                instruction, repository, options, previous_results
            )

            # If no tasks are planned, the instruction is complete
            if not plan.plan_steps:
                break

            # Step 2: Execute
            result = await self.orchestrator.execute(plan)

            # Collect results for memory
            cycle_results = []
            for step in result.execution_steps:
                cycle_results.append(
                    {
                        "step_id": step.get("step_id"),
                        "tool": step.get("tool"),
                        "request": step.get("request"),
                        "response": step.get("response"),
                    }
                )

            previous_results.extend(cycle_results)

            if final_result is None:
                final_result = result
            else:
                # Merge the results (steps, data, etc.)
                final_result.execution_steps.extend(result.execution_steps)
                final_result.execution_plan.extend(result.execution_plan)
                final_result.completed_steps.extend(result.completed_steps)
                final_result.failed_steps.extend(result.failed_steps)
                final_result.api_calls += result.api_calls
                final_result.execution_duration += result.execution_duration

            # If execution failed, we should probably stop or let it replan based on failure
            if result.execution_status != "COMPLETED":
                break

        # If it finished early without executing anything, we need to return something
        if not final_result:
            raise ValueError("Planner did not generate any initial steps.")

        return final_result

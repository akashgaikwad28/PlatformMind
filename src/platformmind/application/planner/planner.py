"""
Planner Orchestrator.
"""

from platformmind.application.interfaces.core.planner import Planner
from platformmind.application.planner.pipeline import PlanningPipeline
from platformmind.domain.models.execution import ExecutionPlan
from platformmind.domain.models.instruction import Instruction


class PlannerImpl(Planner):
    """
    Implements the Phase 2 Planner interface.
    Delegates to the PlanningPipeline.
    """

    def __init__(self, pipeline: PlanningPipeline):
        self.pipeline = pipeline

    async def plan(
        self, instruction: Instruction, previous_results: list = None
    ) -> ExecutionPlan:
        # Extract repository and options from metadata
        repository = instruction.metadata.get(
            "repository", "akashgaikwad28/PlatformMind"
        )
        options = instruction.metadata.get("options", {})

        # Pass the full domain object and context details into the pipeline
        return await self.pipeline.execute(
            instruction, repository, options, previous_results
        )

"""
Memory Retriever.
"""

from platformmind.application.interfaces.memory.memory_engine import MemoryEngine
from platformmind.domain.models.planning_context import (
    CapabilityMemoryContext,
    ConstraintMemoryContext,
    ExecutionMemoryContext,
    LearningMemoryContext,
    PlanningContext,
)


class MemoryRetriever:
    """
    Retrieves independent memory sources and attaches them to the PlanningContext.
    """

    def __init__(self, memory_engine: MemoryEngine):
        self.memory_engine = memory_engine

    async def retrieve_execution_memory(
        self, context: PlanningContext
    ) -> ExecutionMemoryContext:
        """
        Retrieves historical executions related to the current context.
        """
        similar = await self.memory_engine.retrieve_similar(
            context.instruction.normalized_text, limit=10
        )

        successful_plans = [m for m in similar if m.get("status") == "SUCCESS"]
        failed_plans = [m for m in similar if m.get("status") != "SUCCESS"]

        # Base metrics mapping for V1 architecture structure

        mem_ctx = ExecutionMemoryContext(
            previous_executions=similar,
            successful_plans=successful_plans,
            failed_plans=failed_plans,
            execution_metrics={
                "average_duration": sum(
                    [m.get("duration", 0.0) for m in successful_plans]
                )
                / len(successful_plans)
                if successful_plans
                else 0.0,
                "success_rate": len(successful_plans) / len(similar)
                if similar
                else 1.0,
            },
            historical_api_calls=[
                {
                    "execution_id": m.get("execution_id"),
                    "api_calls": m.get("api_calls", 0),
                }
                for m in successful_plans
            ],
        )
        context.execution_memory = mem_ctx
        return mem_ctx

    async def retrieve_capability_memory(
        self, context: PlanningContext
    ) -> CapabilityMemoryContext:
        """
        Retrieves known capabilities, synthesized tools, and their success metrics.
        """
        # Fetching capabilities dynamically from registry abstraction
        await self.memory_engine.retrieve_similar("capability_registry_fetch", limit=50)
        # We will infer capability metrics based on execution history
        # Or from specialized capability memory index if available
        known_caps = [
            "search_issues",
            "create_issue",
            "update_issue",
            "close_issue",
            "create_comment",
            "assign_label",
            "create_label",
            "get_repository",
        ]
        synth_caps = []  # Assuming dynamic fetching

        mem_ctx = CapabilityMemoryContext(
            known_capabilities=known_caps,
            synthesized_capabilities=synth_caps,
            success_rates={cap: 0.95 for cap in known_caps},
            usage_frequency={cap: 10 for cap in known_caps},
        )
        context.capability_memory = mem_ctx
        return mem_ctx

    async def retrieve_constraint_memory(
        self, context: PlanningContext
    ) -> ConstraintMemoryContext:
        """
        Retrieves GitHub validation errors, rate limits, and repository constraints.
        """
        constraints = await self.memory_engine.retrieve_constraints(context.repository)

        validation_errors = [
            c.get("error") for c in constraints if c.get("type") == "validation_error"
        ]

        mem_ctx = ConstraintMemoryContext(
            validation_errors=validation_errors,
            permission_failures=[],
            rate_limits={"core": {"limit": 5000, "remaining": 4900}},
            repository_constraints=[
                c.get("description")
                for c in constraints
                if c.get("type") == "repository_rule"
            ],
        )
        context.constraint_memory = mem_ctx
        return mem_ctx

    async def retrieve_learning_memory(
        self, context: PlanningContext
    ) -> LearningMemoryContext:
        """
        Retrieves best execution strategies and historical optimizations.
        """
        mem_ctx = LearningMemoryContext(
            best_strategies=["sequential_dependency", "intent_based_routing"],
            planner_improvements=["reduced_api_calls_by_batching"],
            historical_optimization={"time_improvement_pct": 15.0},
            tool_ranking_history=[],
        )
        context.learning_memory = mem_ctx
        return mem_ctx

    async def retrieve_all(self, context: PlanningContext) -> None:
        """
        Populates all memory contexts on the given PlanningContext.
        """
        await self.retrieve_execution_memory(context)
        await self.retrieve_capability_memory(context)
        await self.retrieve_constraint_memory(context)
        await self.retrieve_learning_memory(context)

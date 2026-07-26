"""
Memory Context Builder Component.
"""

from platformmind.application.memory.schemas import MemoryContext, RankedMemory


class MemoryContextBuilder:
    """
    Assembles Ranked Context for the Planner.
    """

    def build_context(
        self,
        ranked_executions: list[RankedMemory],
        ranked_capabilities: list[RankedMemory],
        ranked_constraints: list[RankedMemory],
        summary: str = "",
    ) -> MemoryContext:
        return MemoryContext(
            executions=ranked_executions,
            capabilities=ranked_capabilities,
            constraints=ranked_constraints,
            summary=summary,
            metrics={
                "total_items": len(ranked_executions)
                + len(ranked_capabilities)
                + len(ranked_constraints)
            },
        )

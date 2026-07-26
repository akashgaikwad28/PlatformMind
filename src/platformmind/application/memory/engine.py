"""
Memory Engine Implementation.
"""

from typing import Any

from platformmind.application.interfaces.memory.memory_engine import MemoryEngine
from platformmind.application.memory.components.compactor import MemoryCompactor
from platformmind.application.memory.components.context_builder import (
    MemoryContextBuilder,
)
from platformmind.application.memory.components.extractor import KnowledgeExtractor
from platformmind.application.memory.components.ranker import MemoryRanker
from platformmind.application.memory.components.summarizer import MemorySummarizer
from platformmind.application.memory.schemas import RankedMemory
from platformmind.application.memory.services.capability import CapabilityMemoryService
from platformmind.application.memory.services.constraint import ConstraintMemoryService
from platformmind.application.memory.services.execution import ExecutionMemoryService
from platformmind.application.memory.services.learning import LearningMemoryService
from platformmind.domain.models.memory import ExecutionRecord


class MemoryEngineImpl(MemoryEngine):
    def __init__(
        self,
        execution_service: ExecutionMemoryService,
        capability_service: CapabilityMemoryService,
        constraint_service: ConstraintMemoryService,
        learning_service: LearningMemoryService,
        extractor: KnowledgeExtractor,
        ranker: MemoryRanker,
        compactor: MemoryCompactor,
        summarizer: MemorySummarizer,
        context_builder: MemoryContextBuilder,
    ):
        self.execution_service = execution_service
        self.capability_service = capability_service
        self.constraint_service = constraint_service
        self.learning_service = learning_service
        self.extractor = extractor
        self.ranker = ranker
        self.compactor = compactor
        self.summarizer = summarizer
        self.context_builder = context_builder

    async def store_execution(self, execution_data: dict[str, Any]) -> bool:
        # 1. Transform dict to ExecutionRecord (assuming domain validation handles this)
        # For this example, we assume execution_data is already a valid ExecutionRecord instance
        # because the interface defined dict, but we typically use domain models internally.
        record: ExecutionRecord = execution_data["record"]  # A small adapter pattern

        # 2. Extract Knowledge
        constraints = self.extractor.extract_constraints(record)
        capability = self.extractor.extract_capability(record)

        # 3. Update Constraint Memory
        for constraint in constraints:
            await self.constraint_service.store_constraint(constraint)

        # 4. Update Capability Memory
        if capability:
            await self.capability_service.register_capability(capability)

        # 5. Update Learning Metrics
        await self.learning_service.track_metrics(
            {"execution_id": record.execution_id.value}
        )

        # 6. Store Execution Memory & Semantic Memory
        return await self.execution_service.store_execution(record)

    async def retrieve_similar(
        self, query: str, limit: int = 5
    ) -> list[dict[str, Any]]:
        # Returns a combined context
        executions = await self.execution_service.find_similar_executions(query, limit)
        capabilities = await self.capability_service.search_capabilities(query, limit)
        constraints = await self.constraint_service.search_constraints(query, limit)

        # Convert to RankedMemory wrappers for ranking
        ranked_execs = [
            RankedMemory(
                item=e,
                type="execution",
                similarity=0.9,
                recency_score=0.8,
                success_rate=1.0,
            )
            for e in executions
        ]
        ranked_caps = [
            RankedMemory(
                item=c,
                type="capability",
                similarity=0.8,
                recency_score=0.5,
                success_rate=0.9,
            )
            for c in capabilities
        ]
        ranked_cons = [
            RankedMemory(
                item=c,
                type="constraint",
                similarity=0.7,
                recency_score=0.9,
                success_rate=0.0,
            )
            for c in constraints
        ]

        final_execs = self.ranker.rank_memories(ranked_execs)
        final_caps = self.ranker.rank_memories(ranked_caps)
        final_cons = self.ranker.rank_memories(ranked_cons)

        context = self.context_builder.build_context(
            final_execs, final_caps, final_cons, summary="Aggregated context"
        )

        # In a real app we might return the Pydantic model directly, but interface dictates dict
        return [context.model_dump()]

    async def store_capability(self, capability_data: dict[str, Any]) -> bool:
        return await self.capability_service.register_capability(
            capability_data["capability"]
        )

    async def retrieve_capability(self, query: str) -> dict[str, Any]:
        res = await self.capability_service.search_capabilities(query, limit=1)
        return {"capability": res[0]} if res else {}

    async def store_constraint(self, constraint_data: dict[str, Any]) -> bool:
        return await self.constraint_service.store_constraint(
            constraint_data["constraint"]
        )

    async def retrieve_constraints(self, context: str) -> list[dict[str, Any]]:
        cons = await self.constraint_service.search_constraints(context, limit=5)
        return [{"constraint": c} for c in cons]

    async def compact_memory(self) -> bool:
        report = await self.compactor.compact_old_memories()
        return report.summarized_count > 0 or report.archived_count > 0

    async def rank_memories(
        self, memories: list[dict[str, Any]], context: str
    ) -> list[dict[str, Any]]:
        # This implementation expects standard dict mappings
        return memories

    async def summarize(self, memories: list[dict[str, Any]]) -> str:
        return await self.summarizer.summarize_memories(str(memories))

    async def get_memory(self) -> dict[str, Any]:
        history = []
        successful_strats = []
        failed_strats = []
        try:
            recent_execs = await self.execution_service.list_recent()
            for rec in recent_execs:
                history.append(rec.instruction)
                summary = getattr(rec, "execution_summary", "")
                if (
                    getattr(rec, "status", None) == "SUCCESS"
                    or "success" in summary.lower()
                ):
                    successful_strats.append(summary)
                else:
                    failed_strats.append(summary)
        except Exception:
            pass

        known_caps = []
        synth_caps = []
        try:
            caps = (
                await self.capability_service.repository.list()
                if hasattr(self.capability_service, "repository")
                and self.capability_service.repository
                else []
            )
            for c in caps:
                name = getattr(c, "name", str(c))
                if getattr(c, "is_native", True):
                    known_caps.append(name)
                else:
                    synth_caps.append(name)
        except Exception:
            pass

        val_rules = []
        gh_limits = []
        try:
            cons = (
                await self.constraint_service.repository.list()
                if hasattr(self.constraint_service, "repository")
                and self.constraint_service.repository
                else []
            )
            for c in cons:
                val_rules.append(getattr(c, "description", str(c)))
        except Exception:
            pass

        improvements = []
        opt_history = []
        try:
            records = (
                await self.learning_service.repository.list()
                if hasattr(self.learning_service, "repository")
                and self.learning_service.repository
                else []
            )
            for r in records:
                improvements.append(str(r))
        except Exception:
            pass

        total_execs = len(history)
        success_count = len(successful_strats)
        success_rate = round(success_count / total_execs, 2) if total_execs > 0 else 0.0

        return {
            "execution": {
                "history": history,
                "successful_strategies": successful_strats,
                "failed_strategies": failed_strats,
            },
            "capabilities": {
                "known": known_caps,
                "synthesized": synth_caps,
                "success_rate": success_rate,
                "confidence": 1.0 if total_execs > 0 else 0.0,
            },
            "constraints": {
                "validation_rules": val_rules,
                "github_limitations": gh_limits,
                "rate_limits": {},
            },
            "learning": {
                "improvements": improvements,
                "optimization_history": opt_history,
                "planner_evolution": [],
            },
        }

"""
Memory Ranker Component.
"""

from platformmind.application.memory.schemas import RankedMemory


class MemoryRanker:
    """
    Implements the ranking algorithm combining Similarity, Recency, Success Rate, Confidence.
    """

    def rank_memories(self, candidates: list[RankedMemory]) -> list[RankedMemory]:
        ranked = []
        for memory in candidates:
            # 1. Base similarity (0 to 1)
            similarity_weight = 0.5

            # 2. Recency (0 to 1 decay)
            recency_weight = 0.2
            # Calculate recency if timestamp exists

            # 3. Success rate (0 to 1)
            success_weight = 0.2

            # 4. Confidence (0 to 1)
            confidence_weight = 0.1

            score = (
                (memory.similarity * similarity_weight)
                + (memory.recency_score * recency_weight)
                + (memory.success_rate * success_weight)
                + (memory.confidence * confidence_weight)
            )

            # Recreate with final score (because it's frozen)
            ranked_memory = RankedMemory(
                item=memory.item,
                type=memory.type,
                similarity=memory.similarity,
                recency_score=memory.recency_score,
                success_rate=memory.success_rate,
                confidence=memory.confidence,
                final_score=score,
            )
            ranked.append(ranked_memory)

        return sorted(ranked, key=lambda x: x.final_score, reverse=True)

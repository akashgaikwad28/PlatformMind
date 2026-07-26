"""
Execution Memory Service.
"""

from platformmind.application.interfaces.llm.embedding_provider import EmbeddingProvider
from platformmind.application.interfaces.repositories.repositories import (
    ExecutionRepository,
)
from platformmind.application.interfaces.vectorstore.vector_store import VectorStore
from platformmind.domain.models.memory import ExecutionRecord
from platformmind.domain.value_objects import ExecutionId


class ExecutionMemoryService:
    def __init__(
        self,
        repository: ExecutionRepository,
        vector_store: VectorStore,
        embedding_provider: EmbeddingProvider,
    ):
        self.repository = repository
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider

    async def store_execution(self, record: ExecutionRecord) -> bool:
        await self.repository.create(record)
        # Store embedding
        vector = await self.embedding_provider.embed_text(
            record.instruction + " " + record.execution_summary
        )
        await self.vector_store.index(
            vector_id=record.execution_id.value,
            vector=vector,
            payload={"type": "execution", "instruction": record.instruction},
        )
        return True

    async def get_execution(self, execution_id: str) -> ExecutionRecord | None:
        return await self.repository.get_by_id(ExecutionId(value=execution_id))

    async def find_similar_executions(
        self, instruction: str, limit: int = 5
    ) -> list[ExecutionRecord]:
        vector = await self.embedding_provider.embed_text(instruction)
        results = await self.vector_store.search(query_vector=vector, limit=limit)

        records = []
        for res in results:
            if res.get("payload", {}).get("type") == "execution":
                rec = await self.get_execution(res["id"])
                if rec:
                    records.append(rec)
        return records

    async def list_recent(self) -> list[ExecutionRecord]:
        all_records = await self.repository.list()
        return sorted(all_records, key=lambda x: x.timestamp, reverse=True)[:10]

    async def delete_execution(self, execution_id: str) -> bool:
        deleted = await self.repository.delete(ExecutionId(value=execution_id))
        if deleted:
            await self.vector_store.delete(execution_id)
        return deleted

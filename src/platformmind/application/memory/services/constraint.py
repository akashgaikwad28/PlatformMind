"""
Constraint Memory Service.
"""

from platformmind.application.interfaces.llm.embedding_provider import EmbeddingProvider
from platformmind.application.interfaces.repositories.repositories import (
    ConstraintRepository,
)
from platformmind.application.interfaces.vectorstore.vector_store import VectorStore
from platformmind.domain.models.constraint import Constraint


class ConstraintMemoryService:
    def __init__(
        self,
        repository: ConstraintRepository,
        vector_store: VectorStore,
        embedding_provider: EmbeddingProvider,
    ):
        self.repository = repository
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider

    async def store_constraint(self, constraint: Constraint) -> bool:
        exists = await self.repository.exists(constraint.id)
        if exists:
            return False
        await self.repository.create(constraint)

        vector = await self.embedding_provider.embed_text(constraint.description)
        await self.vector_store.index(
            vector_id=constraint.id,
            vector=vector,
            payload={"type": "constraint", "severity": constraint.severity.value},
        )
        return True

    async def retrieve_constraints(self) -> list[Constraint]:
        return await self.repository.list()

    async def search_constraints(self, query: str, limit: int = 5) -> list[Constraint]:
        vector = await self.embedding_provider.embed_text(query)
        results = await self.vector_store.search(query_vector=vector, limit=limit)

        constraints = []
        for res in results:
            if res.get("payload", {}).get("type") == "constraint":
                c = await self.repository.get_by_id(res["id"])
                if c:
                    constraints.append(c)
        return constraints

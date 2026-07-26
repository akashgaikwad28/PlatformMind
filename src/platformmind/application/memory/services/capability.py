"""
Capability Memory Service.
"""

from platformmind.application.interfaces.llm.embedding_provider import EmbeddingProvider
from platformmind.application.interfaces.repositories.repositories import (
    CapabilityRepository,
)
from platformmind.application.interfaces.vectorstore.vector_store import VectorStore
from platformmind.domain.models.capability import Capability
from platformmind.domain.value_objects import CapabilityId


class CapabilityMemoryService:
    def __init__(
        self,
        repository: CapabilityRepository,
        vector_store: VectorStore,
        embedding_provider: EmbeddingProvider,
    ):
        self.repository = repository
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider

    async def register_capability(self, capability: Capability) -> bool:
        exists = await self.repository.exists(capability.id)
        if exists:
            return False
        await self.repository.create(capability)

        vector = await self.embedding_provider.embed_text(capability.description)
        await self.vector_store.index(
            vector_id=capability.id.value,
            vector=vector,
            payload={"type": "capability", "name": capability.name},
        )
        return True

    async def get_capability(self, capability_id: str) -> Capability | None:
        return await self.repository.get_by_id(CapabilityId(value=capability_id))

    async def update_capability(self, capability: Capability) -> bool:
        await self.repository.update(capability.id, capability)
        return True

    async def search_capabilities(self, query: str, limit: int = 5) -> list[Capability]:
        vector = await self.embedding_provider.embed_text(query)
        results = await self.vector_store.search(query_vector=vector, limit=limit)

        capabilities = []
        for res in results:
            if res.get("payload", {}).get("type") == "capability":
                cap = await self.get_capability(res["id"])
                if cap:
                    capabilities.append(cap)
        return capabilities

    async def increment_usage(
        self, capability_id: str, success: bool, execution_time: float
    ) -> None:
        cap = await self.get_capability(capability_id)
        if not cap:
            return

        # Simplified logic for tracking usage metrics
        # (In a real system this would use LearningRepository)
        pass

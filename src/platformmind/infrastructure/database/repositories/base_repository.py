"""
Base generic repository implementation.
"""

from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from platformmind.domain.exceptions.exceptions import RepositoryException

T = TypeVar("T")  # Domain Model
M = TypeVar("M")  # ORM Model
ID = TypeVar("ID")


class BaseRepositoryImpl(Generic[T, M, ID]):
    def __init__(self, session: AsyncSession, model_class: Type[M], mapper: Any):
        self.session = session
        self.model_class = model_class
        self.mapper = mapper

    async def create(self, entity: T) -> T:
        try:
            orm_model = self.mapper.to_orm(entity)
            self.session.add(orm_model)
            # Not committing here; let UOW handle it
            await self.session.flush()
            return self.mapper.to_domain(orm_model)
        except Exception as e:
            raise RepositoryException(f"Failed to create entity: {str(e)}") from e

    async def get_by_id(self, entity_id: ID) -> T | None:
        try:
            pk = getattr(entity_id, "value", entity_id)
            orm_model = await self.session.get(self.model_class, pk)
            if orm_model:
                return self.mapper.to_domain(orm_model)
            return None
        except Exception as e:
            raise RepositoryException(f"Failed to fetch entity by ID: {str(e)}") from e

    async def list(self) -> list[T]:
        try:
            result = await self.session.execute(select(self.model_class))
            orm_models = result.scalars().all()
            return [self.mapper.to_domain(model) for model in orm_models]
        except Exception as e:
            raise RepositoryException(f"Failed to list entities: {str(e)}") from e

    async def update(self, entity_id: ID, entity: T) -> T:
        try:
            pk = getattr(entity_id, "value", entity_id)
            orm_model = await self.session.get(self.model_class, pk)
            if not orm_model:
                raise RepositoryException(f"Entity with ID {entity_id} not found.")

            # Simple replacement merge strategy for updates
            new_orm_model = self.mapper.to_orm(entity)
            new_orm_model.id = pk  # ensure ID matches
            merged_model = await self.session.merge(new_orm_model)
            await self.session.flush()
            return self.mapper.to_domain(merged_model)
        except RepositoryException:
            raise
        except Exception as e:
            raise RepositoryException(f"Failed to update entity: {str(e)}") from e

    async def delete(self, entity_id: ID) -> bool:
        try:
            pk = getattr(entity_id, "value", entity_id)
            orm_model = await self.session.get(self.model_class, pk)
            if not orm_model:
                return False
            await self.session.delete(orm_model)
            await self.session.flush()
            return True
        except Exception as e:
            raise RepositoryException(f"Failed to delete entity: {str(e)}") from e

    async def exists(self, entity_id: ID) -> bool:
        return await self.get_by_id(entity_id) is not None

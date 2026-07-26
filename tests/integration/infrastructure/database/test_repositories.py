import uuid
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from platformmind.domain.models.memory import ExecutionRecord
from platformmind.domain.value_objects import ExecutionId
from platformmind.infrastructure.database.base import Base
from platformmind.infrastructure.database.repositories.repositories import (
    ExecutionRepositoryImpl,
)
from platformmind.infrastructure.database.uow import UnitOfWork

# Use in-memory sqlite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_engine() -> None:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
def test_session_factory(test_engine) -> None:
    return async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )


@pytest.mark.asyncio
async def test_execution_repository_crud(test_session_factory) -> None:
    uow = UnitOfWork(session_factory=test_session_factory)

    test_id = ExecutionId(value=str(uuid.uuid4()))
    record = ExecutionRecord(
        execution_id=test_id,
        instruction="Do something",
        execution_summary="Did something",
        metrics={"time": 1.2},
        timestamp=datetime.now(),
    )

    # 1. CREATE
    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        created = await repo.create(record)
        assert created.execution_id == test_id

    # 2. READ
    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        fetched = await repo.get_by_id(test_id)
        assert fetched is not None
        assert fetched.instruction == "Do something"
        assert fetched.metrics == {"time": 1.2}

    # 3. EXISTS / LIST
    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        assert await repo.exists(test_id) is True
        all_records = await repo.list()
        assert len(all_records) == 1

    # 4. UPDATE
    record_updated = ExecutionRecord(
        execution_id=test_id,
        instruction="Do something else",
        execution_summary="Did something else",
        metrics={"time": 2.0},
        timestamp=datetime.now(),
    )

    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        updated = await repo.update(test_id, record_updated)
        assert updated.instruction == "Do something else"

    # Verify update persisted
    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        fetched2 = await repo.get_by_id(test_id)
        assert fetched2.instruction == "Do something else"  # type: ignore

    # 5. DELETE
    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        assert await repo.delete(test_id) is True

    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        assert await repo.get_by_id(test_id) is None


@pytest.mark.asyncio
async def test_uow_rollback_on_exception(test_session_factory) -> None:
    uow = UnitOfWork(session_factory=test_session_factory)
    test_id = ExecutionId(value=str(uuid.uuid4()))

    record = ExecutionRecord(
        execution_id=test_id,
        instruction="Fail me",
        execution_summary="Failed",
        metrics={},
        timestamp=datetime.now(),
    )

    try:
        async with uow as session:
            repo = ExecutionRepositoryImpl(session)
            await repo.create(record)
            raise ValueError("Intentional crash")
    except ValueError:
        pass  # Expected original error to propagate after rollback

    # Verify it rolled back
    async with uow as session:
        repo = ExecutionRepositoryImpl(session)
        assert await repo.get_by_id(test_id) is None

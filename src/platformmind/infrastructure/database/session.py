"""
Database Session module.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from platformmind.infrastructure.database.connection import engine

async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_session() -> AsyncSession:
    """
    Dependency to get a new async session.
    """
    async with async_session_factory() as session:
        yield session  # type: ignore

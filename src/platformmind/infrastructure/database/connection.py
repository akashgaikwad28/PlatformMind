"""
Database Connection module.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from platformmind.core.config.settings import settings


def get_engine() -> AsyncEngine:
    """
    Creates and returns a SQLAlchemy async engine.
    """
    return create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)


engine = get_engine()

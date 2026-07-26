"""
Unit of Work module.
"""

from types import TracebackType
from typing import Any, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from platformmind.domain.exceptions.exceptions import RepositoryException
from platformmind.infrastructure.database.session import async_session_factory


class UnitOfWork:
    """
    Context manager for database transactions.
    """

    def __init__(self, session_factory: Any = async_session_factory) -> None:
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        self.session = self.session_factory()
        return self.session

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.session is None:
            return

        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise RepositoryException(f"Transaction failed: {str(e)}") from e
        finally:
            await self.session.close()

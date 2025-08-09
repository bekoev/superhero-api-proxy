from __future__ import annotations

from asyncio import current_task
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import Logger

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.plugins.postgres.settings import PostgresSettings


class PostgresPlugin:
    def __init__(self, logger: Logger, config: PostgresSettings):
        self.config = config
        self.engine = create_async_engine(url=self.config.url, **self.config.opts)
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )
        self.logger = logger

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        session: AsyncSession = self._session_factory()

        try:
            yield session
        except Exception as e:
            await session.rollback()

            raise e
        finally:
            await session.close()
            await self._session_factory.remove()

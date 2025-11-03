from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.plugins.postgres.settings import PostgresSettings


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self, config: PostgresSettings) -> AsyncEngine:
        engine = create_async_engine(url=config.url, **config.opts)
        return engine

    @provide(scope=Scope.REQUEST)
    async def session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(engine, autoflush=False) as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e

import logging
from collections.abc import AsyncIterator

import httpx
from dishka import Provider, Scope, from_context, provide

from app.plugins.logger.logging_config import LoggingConfiguration, init_logging
from app.plugins.logger.settings import LoggerSettings
from app.plugins.postgres.settings import PostgresSettings
from app.services.hero import HeroService
from app.services.storage.interface import HeroRepositoryInterface
from app.services.storage.repository import HeroRepository
from app.services.superhero_api import SuperheroApiClient
from app.settings import AppSettings


class AppProvider(Provider):
    logger_settings = from_context(provides=LoggerSettings, scope=Scope.APP)
    app_settings = from_context(provides=AppSettings, scope=Scope.APP)
    postgres_settings = from_context(provides=PostgresSettings, scope=Scope.APP)

    logging_config = provide(LoggingConfiguration, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def logger(self, config: LoggingConfiguration) -> logging.Logger:
        return init_logging(config)

    @provide(scope=Scope.APP)
    async def superhero_http_client(self) -> AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient() as session:
            yield session

    superhero_api_client = provide(SuperheroApiClient, scope=Scope.REQUEST)
    hero_repository = provide(
        HeroRepository, provides=HeroRepositoryInterface, scope=Scope.REQUEST
    )
    hero_service = provide(HeroService, scope=Scope.REQUEST)

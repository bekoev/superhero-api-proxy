import logging
from typing import Annotated

import httpx
from dishka import FromComponent, Provider, Scope, from_context, provide

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

    @provide(scope=Scope.REQUEST)
    def superhero_api_client(
        self,
        superhero_http_client: Annotated[
            httpx.AsyncClient, FromComponent("superhero-api")
        ],
        app_config: AppSettings,
        logger: logging.Logger,
    ) -> SuperheroApiClient:
        return SuperheroApiClient(
            http_client=superhero_http_client, app_config=app_config, logger=logger
        )

    hero_repository = provide(
        HeroRepository, provides=HeroRepositoryInterface, scope=Scope.REQUEST
    )
    hero_service = provide(HeroService, scope=Scope.REQUEST)

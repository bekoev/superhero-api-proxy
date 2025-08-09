from typing import Set

from dependency_injector import containers, providers

from app.plugins.http.http_client import http_client_session
from app.plugins.logger.logging_config import LoggingConfiguration, init_logging
from app.plugins.logger.settings import LoggerSettings
from app.plugins.postgres.plugin import PostgresPlugin
from app.plugins.postgres.settings import PostgresSettings
from app.services.hero import HeroService
from app.services.storage.repository import HeroRepository
from app.services.superhero_api import SuperheroApiClient
from app.settings import AppSettings, MainSettings


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(
        MainSettings,
        logger=LoggerSettings(),
        app=AppSettings(),
        db=PostgresSettings(),
    )

    logging_config = providers.Singleton(
        LoggingConfiguration,
        app_settings=config.provided,
    )
    logger = providers.Singleton(
        init_logging,
        config=logging_config,
    )

    db = providers.Singleton(
        PostgresPlugin,
        logger=logger,
        config=config.provided.db,
    )

    superhero_http_client = providers.Resource(
        http_client_session,
    )
    superhero_api_client = providers.Factory(
        SuperheroApiClient,
        http_client=superhero_http_client,
        app_config=config.provided.app,
        logger=logger.provided,
    )
    # hero_repository = providers.Factory(
    #     HeroRepositoryInMemory,
    # )
    hero_repository = providers.Factory(
        HeroRepository,
        db_session=db.provided.session,
        logger=logger.provided,
    )
    hero_service = providers.Factory(
        HeroService,
        superhero_api_client=superhero_api_client,
        hero_repository=hero_repository,
        logger=logger.provided,
    )


modules: Set = set()
container = Container()


def inject_module(module_name: str):
    modules.add(module_name)


def provide_wire(*wires: list):
    container.wire(modules=modules)

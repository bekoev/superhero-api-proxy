from dishka import Provider, Scope, from_context, make_async_container, provide

from app.plugins.http.ioc_provider import HTTPProvider
from app.plugins.logger.ioc_provider import LoggingProvider
from app.plugins.logger.settings import LoggerSettings
from app.plugins.postgres.ioc_provider import DBProvider
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

    superhero_api_client = provide(SuperheroApiClient, scope=Scope.REQUEST)
    hero_repository = provide(
        HeroRepository, provides=HeroRepositoryInterface, scope=Scope.REQUEST
    )
    hero_service = provide(HeroService, scope=Scope.REQUEST)


def create_container():
    return make_async_container(
        AppProvider(),
        DBProvider(),
        HTTPProvider(),
        LoggingProvider(),
        context={
            LoggerSettings: LoggerSettings(),
            AppSettings: AppSettings(),
            PostgresSettings: PostgresSettings(),
        },
    )

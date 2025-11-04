from app.plugins.logger.settings import LoggerSettings
from app.plugins.postgres.settings import PostgresSettings
from app.services.hero import HeroService
from app.services.storage.interface import HeroRepositoryInterface
from app.services.storage.repository import HeroRepository
from app.services.superhero_api import SuperheroApiClient
from app.settings import AppSettings


from dishka import Provider, Scope, from_context, provide


class AppProvider(Provider):
    logger_settings = from_context(provides=LoggerSettings, scope=Scope.APP)
    app_settings = from_context(provides=AppSettings, scope=Scope.APP)
    postgres_settings = from_context(provides=PostgresSettings, scope=Scope.APP)

    superhero_api_client = provide(SuperheroApiClient, scope=Scope.REQUEST)
    hero_repository = provide(
        HeroRepository, provides=HeroRepositoryInterface, scope=Scope.REQUEST
    )
    hero_service = provide(HeroService, scope=Scope.REQUEST)

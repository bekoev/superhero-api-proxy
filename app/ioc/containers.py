from dishka import make_async_container

from app.ioc.providers.app import AppProvider
from app.ioc.providers.db import DBProvider
from app.ioc.providers.http import HTTPProvider
from app.ioc.providers.logging import LoggingProvider
from app.plugins.logger.settings import LoggerSettings
from app.plugins.postgres.settings import PostgresSettings
from app.settings import AppSettings


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

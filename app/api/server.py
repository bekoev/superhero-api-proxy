from contextlib import asynccontextmanager
from functools import lru_cache
from logging import Logger

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exceptions import add_exceptions
from app.api.routers import add_routers
from app.core.ioc_containers import AppProvider
from app.plugins.logger.settings import LoggerSettings
from app.plugins.postgres.ioc_provider import DBProvider
from app.plugins.postgres.settings import PostgresSettings
from app.settings import AppSettings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger: Logger = await app.state.dishka_container.get(Logger)
    app_settings: AppSettings = await app.state.dishka_container.get(AppSettings)
    logger.info(f"-- Starting {app_settings.name}")

    yield
    logger.info(f"-- Stopping {app_settings.name}")
    await app.state.dishka_container.close()


@lru_cache
def create_app():
    container = make_async_container(
        AppProvider(),
        DBProvider(),
        context={
            LoggerSettings: LoggerSettings(),
            AppSettings: AppSettings(),
            PostgresSettings: PostgresSettings(),
        },
    )

    app_config = AppSettings()
    app = FastAPI(title=app_config.name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exceptions(app)
    add_routers(app)

    setup_dishka(container=container, app=app)

    return app

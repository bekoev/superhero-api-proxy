from contextlib import asynccontextmanager
from logging import Logger

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exceptions import add_exceptions
from app.api.routers import add_routers
from app.ioc.containers import create_container
from app.settings import AppSettings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger: Logger = await app.state.dishka_container.get(Logger)
    app_settings: AppSettings = await app.state.dishka_container.get(AppSettings)
    logger.info(f"-- Starting {app_settings.name}")

    yield
    logger.info(f"-- Stopping {app_settings.name}")
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
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

    return app


def create_production_app() -> FastAPI:
    app = create_app()
    setup_dishka(create_container(), app)
    return app

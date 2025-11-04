from collections.abc import AsyncGenerator, AsyncIterator

import httpx
import pytest
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    ValidationSettings,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import setup_dishka
from sqlalchemy.ext.asyncio import AsyncEngine

from app.api.server import create_app
from app.ioc.providers.app import AppProvider
from app.ioc.providers.db import DBProvider
from app.ioc.providers.logging import LoggingProvider
from app.plugins.logger.settings import LoggerSettings
from app.plugins.postgres.settings import PostgresSettings
from app.settings import AppSettings
from tests.integration.utils.mocks.http_client import SuperheroAPIHTTPMock


class MockHTTPProvider(Provider):
    superhero_http_client = provide(
        provides=httpx.AsyncClient,
        source=SuperheroAPIHTTPMock,
        scope=Scope.APP,
    )


@pytest.fixture(scope="session")
async def app_container() -> AsyncIterator[AsyncContainer]:
    settings = ValidationSettings(
        nothing_overridden=True,
        implicit_override=True,
        nothing_decorated=True,
    )

    container = make_async_container(
        AppProvider(),
        DBProvider(),
        LoggingProvider(),
        MockHTTPProvider(),
        context={
            LoggerSettings: LoggerSettings(),
            AppSettings: AppSettings(),
            PostgresSettings: PostgresSettings(
                # Point tests to a separate database
                db="autotest",
            ),
        },
        # Optional IoC container validation
        validation_settings=settings,
    )
    yield container
    await container.close()


@pytest.fixture(scope="session")
def app(app_container):
    app = create_app()
    setup_dishka(app_container, app)
    return app


@pytest.fixture(scope="session")
async def app_client(app) -> AsyncGenerator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://0.0.0.0") as ac:
        yield ac


@pytest.fixture()
async def db_engine(app_container: AsyncContainer) -> AsyncEngine:
    return await app_container.get(AsyncEngine)

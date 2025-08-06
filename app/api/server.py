from functools import lru_cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exceptions import add_exceptions
from app.api.routers import add_routers
from app.core.containers import Container, provide_wire


@lru_cache
def create_app(container: Container):
    app_config = container.config().app
    app = FastAPI(title=app_config.name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    provide_wire()

    add_exceptions(app)
    add_routers(app)

    app.state.container = container

    return app

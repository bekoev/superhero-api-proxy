from fastapi import APIRouter, FastAPI

from app.routers.hero import hero_router

router = APIRouter(
    tags=["superhero-api-proxy"],
)


def add_routers(app: FastAPI):
    routers = [
        hero_router,
    ]
    for router in routers:
        app.include_router(router)

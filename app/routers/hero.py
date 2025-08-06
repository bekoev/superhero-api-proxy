from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from app.core.containers import Container, inject_module
from app.models.hero import FilterParams, Hero
from app.services.hero import HeroService

inject_module(__name__)


hero_router = APIRouter(
    responses={404: {"messages": "Not found"}},
    tags=["hero"],
)


@hero_router.post("/hero/", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def enlist_hero(
    name: str,
    hero_service: HeroService = Depends(Provide[Container.hero_service]),
) -> None:
    await hero_service.enlist_hero(name)


@hero_router.get(
    "/hero/",
)
@inject
async def find_heroes(
    filter_params: Annotated[FilterParams, Query()],
    hero_service: HeroService = Depends(Provide[Container.hero_service]),
) -> list[Hero]:
    return await hero_service.get_heroes(filter_params)

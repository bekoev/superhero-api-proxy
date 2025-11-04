from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status

from app.models.api.hero import FilterParams, Hero
from app.services.hero import HeroService

hero_router = APIRouter(
    responses={404: {"messages": "Not found"}},
    tags=["hero"],
)


@hero_router.post("/hero/", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def enlist_hero(
    name: str,
    hero_service: FromDishka[HeroService],
) -> None:
    await hero_service.enlist_hero(name)


@hero_router.get(
    "/hero/",
)
@inject
async def find_heroes(
    filter_params: Annotated[FilterParams, Query()],
    hero_service: FromDishka[HeroService],
) -> list[Hero]:
    return await hero_service.get_heroes(filter_params)

from contextlib import AbstractAsyncContextManager
from logging import Logger
from typing import Callable

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.api.hero import FilterParams, Hero
from app.models.db.hero import HeroDB, PowerStatsDB
from app.services.storage.interface import HeroRepositoryInterface


class HeroRepository(HeroRepositoryInterface):
    def __init__(
        self,
        db_session: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        logger: Logger,
    ):
        self.db_session: Callable[..., AbstractAsyncContextManager[AsyncSession]] = (
            db_session
        )
        self.logger = logger

    async def add_hero(self, hero: Hero) -> None:
        async with self.db_session() as session:
            hero_db = HeroDB(
                id=hero.id,
                name=hero.name,
                powerstats=PowerStatsDB(
                    intelligence=hero.powerstats.intelligence,
                    strength=hero.powerstats.strength,
                    speed=hero.powerstats.speed,
                    power=hero.powerstats.power,
                ),
            )
            session.add(hero_db)
            await session.commit()

    async def get_heroes(self, filter_params: FilterParams) -> list[Hero]:
        return []

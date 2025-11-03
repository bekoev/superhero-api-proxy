from logging import Logger

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.api.hero import FilterParams, Hero
from app.models.db.hero import HeroDB, PowerStatsDB
from app.services.storage.interface import HeroRepositoryInterface


class HeroRepository(HeroRepositoryInterface):
    def __init__(
        self,
        db_session: AsyncSession,
        logger: Logger,
    ):
        self.db_session = db_session
        self.logger = logger

    async def add_hero(self, hero: Hero) -> None:
        powerstats = PowerStatsDB(
            intelligence=hero.powerstats.intelligence,
            strength=hero.powerstats.strength,
            speed=hero.powerstats.speed,
            power=hero.powerstats.power,
        )

        # TODO: Evaluate the implementation using PG-specific
        # "upserts" (consider complexity, readability, supportability)
        existing_hero = (
            await self.db_session.execute(select(HeroDB).where(HeroDB.id == hero.id))
        ).scalar_one_or_none()
        if existing_hero:
            existing_hero.name = hero.name
            existing_hero.powerstats = powerstats
        else:
            hero_db = HeroDB(
                id=hero.id,
                name=hero.name,
                powerstats=powerstats,
            )
            self.db_session.add(hero_db)

        await self.db_session.commit()

    async def get_heroes(self, filter_params: FilterParams) -> list[Hero]:
        query = select(HeroDB).join(PowerStatsDB, HeroDB.id == PowerStatsDB.hero_id)
        if filter_params.name is not None:
            query = query.where(HeroDB.name == filter_params.name)
        if filter_params.strengthFrom is not None:
            query = query.where(PowerStatsDB.strength >= filter_params.strengthFrom)
        if filter_params.strengthTo is not None:
            query = query.where(PowerStatsDB.strength <= filter_params.strengthTo)
        if filter_params.intelligenceFrom is not None:
            query = query.where(
                PowerStatsDB.intelligence >= filter_params.intelligenceFrom
            )
        if filter_params.intelligenceTo is not None:
            query = query.where(
                PowerStatsDB.intelligence <= filter_params.intelligenceTo
            )
        if filter_params.speedFrom is not None:
            query = query.where(PowerStatsDB.speed >= filter_params.speedFrom)
        if filter_params.speedTo is not None:
            query = query.where(PowerStatsDB.speed <= filter_params.speedTo)
        if filter_params.powerFrom is not None:
            query = query.where(PowerStatsDB.power >= filter_params.powerFrom)
        if filter_params.powerTo is not None:
            query = query.where(PowerStatsDB.power <= filter_params.powerTo)

        result = await self.db_session.execute(query)
        heroes = result.scalars().all()
        return [Hero.model_validate(hero, from_attributes=True) for hero in heroes]

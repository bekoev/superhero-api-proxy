import logging

from app.api.errors import HeroNotFoundError, MultipleHeroesFoundError
from app.models.hero import FilterParams, Hero
from app.services.storage.repo_inmemory import HeroRepositoryInMemory
from app.services.superhero_api import SuperheroApiClient


class HeroService:
    def __init__(
        self,
        superhero_api_client: SuperheroApiClient,
        hero_repository: HeroRepositoryInMemory,
        logger: logging.Logger,
    ):
        self._logger = logger
        self._superheroes_api = superhero_api_client
        self._heroes_repo = hero_repository

    async def enlist_hero(self, name: str) -> None:
        self._logger.info(f"Looking for hero: {name=}")
        heroes_found = await self._superheroes_api.search_hero(name)

        if not heroes_found:
            self._logger.info(f"Hero {name=} not found")
            raise HeroNotFoundError(name)

        if len(heroes_found) > 1:
            self._logger.info(f"Multiple heroes found for {name=}")
            names = ", ".join([hero.name for hero in heroes_found])
            message = f"Multiple heroes found, specify the name from: {names}"
            raise MultipleHeroesFoundError(message)

        hero = heroes_found[0]
        self._logger.info(f"Hero {name=} found: {hero}")
        await self._heroes_repo.add_hero(hero)

    async def get_heroes(self, filter_params: FilterParams) -> list[Hero]:
        return await self._heroes_repo.get_heroes(filter_params)

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

        # Consider the case when a search on 'black widow' returns
        #  'Black Widow' and 'Black Widow II'.
        hero_found = next(
            filter(lambda hero: hero.name.casefold() == name.casefold(), heroes_found),
            None,
        )

        if not hero_found:
            if len(heroes_found) > 1:
                self._logger.info(f"Multiple heroes found for {name=}")
                names = ", ".join([hero.name for hero in heroes_found])
                message = f"Multiple heroes found, specify the name from: {names}"
                raise MultipleHeroesFoundError(message)
            else:
                self._logger.info(f"Hero {name=} not found")
                raise HeroNotFoundError(name)

        self._logger.info(f"Hero {name=} found: {hero_found}")
        await self._heroes_repo.add_hero(hero_found)

    async def get_heroes(self, filter_params: FilterParams) -> list[Hero]:
        return await self._heroes_repo.get_heroes(filter_params)

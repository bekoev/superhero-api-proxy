from abc import ABC, abstractmethod

from app.models.api.hero import FilterParams, Hero


class HeroRepositoryInterface(ABC):
    @abstractmethod
    async def add_hero(self, hero: Hero) -> None: ...

    @abstractmethod
    async def get_heroes(self, filter_params: FilterParams) -> list[Hero]: ...

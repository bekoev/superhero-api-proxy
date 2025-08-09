from app.models.api.hero import FilterParams, Hero
from app.services.storage.interface import HeroRepositoryInterface

_heroes: dict[int, Hero] = {}


class HeroRepositoryInMemory(HeroRepositoryInterface):
    """In-memory implementation of the hero repository.

    The implementation is kept for testing purposes.
    """

    def __init__(self):
        pass

    # async is for the future, when we will use a database
    async def get_heroes(
        self,
        filter_params: FilterParams,
    ) -> list[Hero]:
        fp = filter_params
        result = []
        for h in _heroes.values():
            if fp.name is not None and fp.name.casefold() != h.name.casefold():
                continue
            if fp.intelligenceFrom is not None and (
                h.powerstats.intelligence is None
                or h.powerstats.intelligence < fp.intelligenceFrom
            ):
                continue
            if fp.intelligenceTo is not None and (
                h.powerstats.intelligence is None
                or h.powerstats.intelligence > fp.intelligenceTo
            ):
                continue
            if fp.strengthFrom is not None and (
                h.powerstats.strength is None or h.powerstats.strength < fp.strengthFrom
            ):
                continue
            if fp.strengthTo is not None and (
                h.powerstats.strength is None or h.powerstats.strength > fp.strengthTo
            ):
                continue
            if fp.speedFrom is not None and (
                h.powerstats.speed is None or h.powerstats.speed < fp.speedFrom
            ):
                continue
            if fp.speedTo is not None and (
                h.powerstats.speed is None or h.powerstats.speed > fp.speedTo
            ):
                continue
            if fp.powerFrom is not None and (
                h.powerstats.power is None or h.powerstats.power < fp.powerFrom
            ):
                continue
            if fp.powerTo is not None and (
                h.powerstats.power is None or h.powerstats.power > fp.powerTo
            ):
                continue
            result.append(h)
        return result

    # async is for the future, when we will use a database
    async def add_hero(self, hero: Hero) -> None:
        _heroes[hero.id] = hero

    # Method to clear all heroes (useful for testing)
    async def clear_all_heroes(self) -> None:
        _heroes.clear()

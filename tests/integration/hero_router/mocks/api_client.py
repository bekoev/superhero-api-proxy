from app.models.hero import Hero, PowerStats


class SuperheroApiClientMock:
    async def search_hero(self, name: str) -> list[Hero]:
        if name.casefold() in "batman":
            return [
                Hero(
                    id=1,
                    name="Batman",
                    powerstats=PowerStats(
                        intelligence=100, strength=100, speed=100, power=100
                    ),
                )
            ]
        else:
            return []

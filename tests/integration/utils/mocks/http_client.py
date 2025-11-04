import json
from pathlib import Path


class MockResponse:
    def __init__(self, status_code: int, json_data: dict):
        self.status_code = status_code
        self._json_data = json_data

    def json(self) -> dict:
        return self._json_data


class SuperheroAPIHTTPMock:
    def __init__(self):
        self._heroes_database = self._load_heroes_database()

    def _load_heroes_database(self) -> list[dict]:
        """Load all heroes from the real API search 'a' response to use as a mock database."""

        mock_dir = Path(__file__).parent
        search_a_file = mock_dir / "api_response_search_a.json"

        heroes = []
        if search_a_file.exists():
            with open(search_a_file, "r") as f:
                data = json.load(f)
                heroes = data.get("results", [])

        return heroes

    def _search_heroes(self, search_term: str) -> list[dict]:
        """Search heroes by name."""

        if not search_term:
            return []

        search_lower = search_term.lower()
        matching_heroes = []

        for hero in self._heroes_database:
            # Check if search term matches hero name
            hero_name = hero.get("name", "").lower()
            if search_lower in hero_name:
                matching_heroes.append(hero)
                continue

        return matching_heroes

    async def get(self, url: str) -> MockResponse:
        """Mock GET method that returns appropriate responses based on URL."""

        # Extract search term from URL pattern: {base_url}/{access_token}/search/{name}
        if "/search/" in url:
            search_term = url.split("/search/")[-1]

        if search_term:
            # Search for matching heroes
            matching_heroes = self._search_heroes(search_term)

            # Return response in the expected format
            if matching_heroes:
                response_data = {
                    "response": "success",
                    "results-for": search_term,
                    "results": matching_heroes,
                }
            else:
                response_data = {
                    "response": "error",
                    "error": "character with given name not found",
                }

            return MockResponse(200, response_data)

        # For any other URL, return 404
        return MockResponse(
            404, {"response": "error", "error": "bad name search request"}
        )

    # async def __aenter__(self):
    #     return self

    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     pass

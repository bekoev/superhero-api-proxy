import logging
from urllib.parse import urljoin

from httpx import AsyncClient
from pydantic import TypeAdapter

from app.models.api.hero import Hero
from app.settings import AppSettings


class SuperheroApiClient:
    def __init__(
        self,
        http_client: AsyncClient,
        app_config: AppSettings,
        logger: logging.Logger,
    ):
        self._logger = logger
        self._http_client = http_client
        self._base_url = app_config.superhero_api_base_url
        self._access_token = app_config.superhero_api_access_token

    async def search_hero(self, name: str) -> list[Hero]:
        url = urljoin(self._base_url, f"{self._access_token}/search/{name}")

        response = await self._http_client.get(url)
        if response.status_code != 200:
            self._logger.error(f"Failed to search for hero: {response.status_code}")
            return []

        response_json = response.json()
        if response_json.get("response") != "success":
            self._logger.error(f"Failed to search for hero: {response_json}")
            return []

        return TypeAdapter(list[Hero]).validate_python(response_json["results"])

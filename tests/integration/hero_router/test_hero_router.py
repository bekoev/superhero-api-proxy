import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "name,expected_status",
    [
        pytest.param("batman", status.HTTP_204_NO_CONTENT, id="known_hero"),
        pytest.param("superman", status.HTTP_404_NOT_FOUND, id="unknown_hero"),
    ],
)
async def test_enlisting_hero(
    app_client: AsyncClient,
    name: str,
    expected_status: int,
):
    """Enlisting a hero."""

    response = await app_client.post(f"/hero/?name={name}")

    assert response.status_code == expected_status

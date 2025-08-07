import pytest

from tests.integration.hero_router.mocks.http_client import SuperheroAPIHTTPMock


@pytest.mark.parametrize(
    "term,expected_status_code,expected_response,expected_results_count",
    [
        # As the sample database was retrieved as search 'a' response:
        pytest.param("batman", 200, "success", 3),
        pytest.param("a-bomb", 200, "success", 1),
        pytest.param("superman", 200, "success", 2),
        pytest.param("man", 200, "success", 65),
        pytest.param("invalid", 200, "error", None),
        pytest.param("", 404, "error", None),
    ],
)
async def test_search(
    term: str,
    expected_status_code: int,
    expected_response: str,
    expected_results_count: int | None,
):
    mock = SuperheroAPIHTTPMock()

    response = await mock.get(f"https://superheroapi.com/api/123/search/{term}")
    data = response.json()
    assert response.status_code == expected_status_code
    assert data.get("response") == expected_response
    if expected_response == "success":
        results = data["results"]
        assert len(results) == expected_results_count

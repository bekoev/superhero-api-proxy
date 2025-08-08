import pytest

from app.core.containers import Container
from tests.integration.hero_router.mocks.http_client import SuperheroAPIHTTPMock

# @pytest.fixture(autouse=True)
# async def prepare_db_data(db_client):
#     """Prepare test DB for tests."""

#     restore_db = DbTestDataHandler(db_client)

#     await restore_db.clear_database()
#     await restore_db.seed_database()
#     yield
#     await restore_db.clear_database()


@pytest.fixture(autouse=True)
def mock_superhero_api_http_client(app_container: Container):
    app_container.superhero_http_client.override(SuperheroAPIHTTPMock())
    yield
    app_container.superhero_http_client.reset_override()


@pytest.fixture(autouse=True)
async def clear_hero_database(app_container: Container):
    """Clear the hero database before each test to ensure test isolation."""
    hero_repo = app_container.hero_repository()
    await hero_repo.clear_all_heroes()
    yield
    # Optionally clear after test as well for cleanliness
    await hero_repo.clear_all_heroes()

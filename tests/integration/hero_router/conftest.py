import pytest

from app.core.containers import Container
from tests.integration.hero_router.mocks.api_client import SuperheroApiClientMock

# @pytest.fixture(autouse=True)
# async def prepare_db_data(db_client):
#     """Prepare test DB for tests."""

#     restore_db = DbTestDataHandler(db_client)

#     await restore_db.clear_database()
#     await restore_db.seed_database()
#     yield
#     await restore_db.clear_database()


@pytest.fixture(autouse=True)
def mock_superhero_api_client(app_container: Container):
    app_container.superhero_api_client.override(SuperheroApiClientMock())
    yield
    app_container.superhero_api_client.reset_override()

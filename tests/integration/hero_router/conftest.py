import pytest
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models.db.hero import HeroDB, PowerStatsDB
from tests.integration.utils.db.db_seeder import DbTestDataHandler


@pytest.fixture(autouse=True)
async def prepare_db_data(db_engine: AsyncEngine):
    """Prepare test DB for tests."""

    db_handler = DbTestDataHandler(db_engine)
    db_handler.add_table_data(HeroDB, [])
    db_handler.add_table_data(PowerStatsDB, [])

    await db_handler.clear_database()
    await db_handler.seed_database()
    yield
    await db_handler.clear_database()

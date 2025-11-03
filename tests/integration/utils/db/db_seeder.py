from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


@dataclass
class DBModelInfo:
    type: Any
    data: list[dict]


class DbTestDataHandler:
    """A class that initializes a DB with test data, and cleans it up afterwards."""

    def __init__(
        self,
        db_engine: AsyncEngine,
        object_type: Any = None,
        table_data: list[dict] | None = None,
    ):
        """Initialize the data handler.

        Also note the add_table_data() possibility to handle another table.
        """
        self._engine = db_engine
        self._tables_handled: list[DBModelInfo] = []
        if object_type is not None and table_data is not None:
            self._tables_handled.append(DBModelInfo(object_type, table_data))

    def add_table_data(self, object_type, table_data: list[dict]):
        """Add a table to handle."""

        self._tables_handled.append(DBModelInfo(object_type, table_data))

    async def clear_database(self):
        """Clear the DB from any tables being handled."""

        async with self._engine.begin() as connection:
            for table_info in reversed(self._tables_handled):
                await connection.run_sync(
                    table_info.type.__table__.drop, checkfirst=True
                )

    async def seed_database(self):
        """Populate the DB with the initial data."""

        async with self._engine.begin() as connection:
            for table_info in self._tables_handled:
                await connection.run_sync(table_info.type.__table__.create)

        async with AsyncSession(self._engine, autoflush=False) as session:
            try:
                for table_info in self._tables_handled:
                    for model in table_info.data:
                        db_object = table_info.type(**model)
                        session.add(db_object)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

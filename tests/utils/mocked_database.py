"""Mocked Database."""
from sqlalchemy import MetaData

from src.db import Base, Database


class MockedDatabase(Database):
    """Mocked database is used for integration tests."""

    async def teardown(self):
        """Clear all data in the database."""
        metadata: MetaData = Base.metadata  # noqa
        for table in metadata.sorted_tables:
            await self.session.execute(table.delete())
        await self.session.commit()

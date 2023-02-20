from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Database, Base


class TestDatabase(Database):

    async def teardown(self):
        """ Clear all data in the database """
        metadata: MetaData = Base.metadata
        async with self.pool() as session:  # type: AsyncSession
            for table in metadata.tables.values():
                await session.execute(table.delete())

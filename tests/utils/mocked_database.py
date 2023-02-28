from sqlalchemy import MetaData

from src.db import Base, Database


class MockedDatabase(Database):
    async def teardown(self):
        """Clear all data in the database"""
        metadata: MetaData = Base.metadata
        for table in metadata.tables.values():
            await self.session.execute(table.delete())
        await self.session.commit()

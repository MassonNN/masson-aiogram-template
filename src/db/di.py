from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.configuration import Configuration
from src.db.database import create_async_engine, Database


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, conf: Configuration) -> AsyncEngine:
        return create_async_engine(conf.db.build_connection_str(), debug=conf.debug)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(bind=engine, autoflush=False) as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_database(self, session: AsyncSession) -> AsyncIterable[Database]:
        yield Database(session=session)


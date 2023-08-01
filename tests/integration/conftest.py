"""Configuration for integrational tests."""
import pytest
import pytest_asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.bot.dispatcher import get_dispatcher
from tests.utils.mocked_bot import MockedBot
from tests.utils.mocked_database import MockedDatabase


@pytest_asyncio.fixture(scope='function')
async def session(engine: AsyncEngine) -> AsyncSession:
    """Async session fixture.

    :param engine: Bind engine for open session
    """
    async with AsyncSession(bind=engine) as session:
        yield session


@pytest_asyncio.fixture(scope='function')
async def db(session: AsyncSession):
    """Database fixture."""
    database = MockedDatabase(session)
    yield database
    await database.teardown()


@pytest.fixture()
def bot():
    """Bot fixture."""
    return MockedBot()


@pytest.fixture()
def storage():
    """Storage fixture."""
    return MemoryStorage()


@pytest.fixture()
def dp(storage):
    """Dispatcher fixture."""
    return get_dispatcher(storage=storage)

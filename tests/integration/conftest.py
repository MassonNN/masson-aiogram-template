"""Configuration for integrational tests."""
from collections.abc import Callable

import pytest
import pytest_asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.dispatcher import get_dispatcher
from src.db.database import create_session_maker
from tests.utils.mocked_bot import MockedBot
from tests.utils.mocked_database import MockedDatabase


@pytest_asyncio.fixture()
async def pool():
    """Pool (sessionmaker) fixture."""
    pool = create_session_maker()
    yield pool
    await pool.close_all()  # noqa


@pytest_asyncio.fixture()
async def db(pool: Callable[[], AsyncSession]):
    """Database fixture."""
    async with pool() as session:  # type: AsyncSession
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

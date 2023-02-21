from typing import Callable

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import create_session_maker
from tests.utils.mocked_database import MockedDatabase


@pytest_asyncio.fixture()
async def pool():
    pool = create_session_maker()
    yield pool
    await pool.close_all()  # noqa


@pytest_asyncio.fixture()
async def db(pool: Callable[[], AsyncSession]):
    session = pool()
    database = MockedDatabase(session)
    yield database
    await database.teardown()
    await session.close()

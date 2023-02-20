import asyncio

import pytest
import pytest_asyncio

from configuration import conf
from tests.utils.test_database import TestDatabase
from utils.alembic import alembic_config_from_url


@pytest_asyncio.fixture()
async def db():
    database = TestDatabase()
    yield database
    await database.teardown()


@pytest.fixture(scope="session")
def event_loop():
    """ Fixture for event loop """
    return asyncio.new_event_loop()


@pytest.fixture()
def alembic_config():
    """
    Alembic configuration object, bound to temporary database.
    """
    return alembic_config_from_url(conf.db.get_url())
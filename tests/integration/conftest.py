"""Configuration for integrational tests."""
import pytest
import pytest_asyncio
from aiogram import Dispatcher
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from src.bot.di import (ConfigurationProvider, FSMStorageProvider,
                        InfrastructureProvider)
from src.bot.dispatcher import setup_dispatcher
from src.db.di import DatabaseProvider
from tests.utils.mocked_bot import MockedBot


@pytest_asyncio.fixture(scope="session")
async def container():
    return make_async_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        ConfigurationProvider(),
        FSMStorageProvider(),
    )


@pytest.fixture()
def bot():
    """Bot fixture."""
    return MockedBot()


@pytest.fixture()
def dp(container):
    """Dispatcher fixture."""
    dp = Dispatcher()
    setup_dishka(container=container, router=dp)
    setup_dispatcher(dp)
    return dp

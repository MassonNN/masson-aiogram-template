import pytest

from src.cache import Cache
from tests.utils.mocked_redis import MockedRedis


@pytest.fixture()
def cache():
    yield Cache(redis=MockedRedis())


@pytest.mark.parametrize(
    'name,value', (
            (name, value) for name in list(map(chr, range(97, 101))) for value in range(10)
    )
)
@pytest.mark.asyncio
async def test_cache_set(cache: Cache, name, value):
    await cache.set(name, value)
    assert value == await cache.get(name)


@pytest.mark.parametrize(
    'value', (
            123, '123', (1, 2, 3), [1, 2, 3], 0x123
    )
)
@pytest.mark.asyncio
async def test_cache_set_any(cache: Cache, value):
    test_name = 'some_name'
    await cache.set(test_name, value)
    assert value == await cache.get(test_name)

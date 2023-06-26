
import pytest
from redis.asyncio.client import Redis

from cache import Cache
from cache.adapter import KeyLike
from language.enums import Locales
from language.translator import LocaleScheme


@pytest.fixture()
def cache():
    class FakeRedis(Redis):
        def __init__(self):
            super().__init__()
            self.storage = {}

        async def get(self, key: KeyLike):
            return self.storage.get(key)

        async def set(self, name: KeyLike, value: str):  #
            self.storage[name] = str(value)

        async def exists(self, keys: list[KeyLike]):
            return all(key in self.storage for key in keys)

        async def teardown(self):
            del self.storage

    fake_redis = FakeRedis()
    cache = Cache(redis=fake_redis)
    yield cache
    fake_redis.teardown()


@pytest.mark.parametrize("value", (Locales.RU, Locales.EN, Locales.UK))
@pytest.mark.asyncio
async def test_cache_set(cache, value):
    await cache.set(key=1, value=value)
    res = await cache.get(key=1)
    assert res == value


@pytest.mark.parametrize(
    "locale,expected",
    (
        (Locales.RU, LocaleScheme(user_id=1, locale=Locales.RU)),
        (Locales.EN, LocaleScheme(user_id=1, locale=Locales.EN)),
        (Locales.UK, LocaleScheme(user_id=1, locale=Locales.UK)),
    ),
)
@pytest.mark.asyncio
async def test_cache_set_locale(cache, locale, expected):
    await cache.set(LocaleScheme(locale=locale, user_id=1))
    res = await cache.get(LocaleScheme(user_id=1))
    assert res == expected

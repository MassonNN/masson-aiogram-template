"""This file contains the cache adapter."""
import asyncio
from typing import Any, TypeVar, final, overload

from redis.asyncio.client import Redis

from src.configuration import conf
from src.language.translator import LocaleScheme

KeyLike = TypeVar("KeyLike", str, LocaleScheme)


def build_redis_client() -> Redis:
    """Build redis client."""
    client = Redis(
        host=conf.redis.host,
        db=conf.redis.db,
        port=conf.redis.port,
        password=conf.redis.passwd,
        username=conf.redis.username,
    )
    asyncio.create_task(client.ping())
    return client


class Cache:
    """Cache adapter."""

    def __init__(self, redis: Redis | dict | None = None):
        """Initialize a Cache adapter with given Redis client.

        :param redis: Redis client instance
        """
        self.client = redis or build_redis_client()

    @property
    def redis_client(self) -> Redis:
        """Redis client which used in the cache adapter.

        :return: Redis client
        """
        return self.client

    @final
    async def get(self, key: KeyLike) -> Any:
        """Get a value from cache database.

        :param key:
        :return: Value.
        """
        if isinstance(key, LocaleScheme):
            key = key.as_key()
        get = await self.client.get(str(key))
        if LocaleScheme.is_locale_scheme(key):
            return LocaleScheme.from_value(key=key, value=get)
        else:
            return get

    @final
    async def set(self, key: KeyLike, value: Any = None):
        """Set a value to cache database.

        :param key: Key to set
        :param value: Value in a serializable type
        :return: Nothing.
        """
        if isinstance(key, LocaleScheme):
            await self.client.set(name=key.as_key(), value=key.as_value())  # noqa
        else:
            await self.client.set(name=str(key), value=value)  # noqa

    @overload
    async def exists(self, key: KeyLike):
        ...

    @overload
    async def exists(self, *keys: list[KeyLike]):
        ...

    async def exists(self, keys: KeyLike | list[KeyLike]):
        """Exists implementation in adapter."""
        if not isinstance(keys, list):
            return await self.client.exists(
                [
                    str(keys),
                ]
            )  # noqa
        else:
            return await self.client.exists(*list(map(str, keys)))  # noqa

""" This file contains the cache adapter """
import asyncio
from typing import Any, List, Optional, TypeVar, final, overload

from redis.asyncio.client import Redis

from src.configuration import conf
from src.language.translator import LocaleScheme

KeyLike = TypeVar("KeyLike", str, LocaleScheme)


def build_redis_client() -> Redis:
    """Build redis client"""
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
    """Cache adapter"""

    def __init__(self, redis: Optional[Redis] = None):
        self.client = redis or build_redis_client()

    @property
    def redis_client(self) -> Redis:
        """
        Redis client which used in the cache adapter
        :return:
        """
        return self.client

    @final
    async def get(self, key: KeyLike) -> Any:
        """
        Get a value from cache database
        :param key:
        :return: Value
        """
        return await self.client.get(str(key))

    @final
    async def set(self, key: KeyLike, value: Any):
        """
        Set a value to cache database
        :param key: Key to set
        :param value: Value in a serializable type
        :return: Nothing
        """
        await self.client.set(name=str(key), value=value)  # noqa

    @overload
    async def exists(self, key: KeyLike):
        """
        Check whether key has already defined or not
        :param key:
        :return: (bool) Result
        """
        ...

    @overload
    async def exists(self, *keys: List[KeyLike]):
        """
        Overload of method to check many keys
        :param keys:
        :return:
        """
        ...

    async def exists(self, keys: KeyLike | List[KeyLike]):
        if not isinstance(keys, list):
            return await self.client.exists(
                [
                    str(keys),
                ]
            )  # noqa
        else:
            return await self.client.exists(*list(map(str, keys)))  # noqa

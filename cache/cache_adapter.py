""" This file contains the cache adapter """
from typing import Optional, Any, TypeVar, List, overload

from redis.asyncio.client import Redis

from abstract import Adapter
from configuration import conf
from language import LocaleScheme


KeyLike = TypeVar('KeyLike', str, LocaleScheme)


def build_redis_client() -> Redis:
    """ Build redis client """
    return Redis(
        host=conf.redis.host,
        db=conf.redis.db,
        port=conf.redis.port,
        password=conf.redis.passwd,
        username=conf.redis.username
    )


class Cache(Adapter):
    """ Cache adapter """

    def __init__(self, redis: Optional[Redis] = None):
        self.client = redis

    @property
    def redis_client(self) -> Redis:
        """
        Redis client which used in the cache adapter
        :return:
        """
        return self.client

    async def get(self, key: KeyLike) -> Any:
        """
        Get a value from cache database
        :param key:
        :return: Value
        """
        return await self.client.get(str(key))

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
        return await self.client.exists([str(key),])  # noqa

    async def exists(self, *keys: List[KeyLike]):
        """
        Overload of method to check many keys
        :param keys:
        :return:
        """
        return await self.client.exists(list(map(str, keys)))  # noqa

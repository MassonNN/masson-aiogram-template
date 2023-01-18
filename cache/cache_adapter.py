""" This file contains the cache adapter """
from typing import Optional, Any, Hashable

from redis.asyncio.client import Redis

from abstract import Adapter
from configuration import conf
from language import LocaleScheme


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

    async def get(self, key: str | LocaleScheme) -> Any:
        """
        Get a value from cache database
        :param key:
        :return: Value
        """
        return await self.client.get(str(key))

    async def set(self, key: Hashable, value: Any):
        """
        Set a value to cache database
        :param key: Key to set
        :param value: Value in a serializable type
        :return: Nothing
        """
        await self.client.set(name=key, value=value)  # noqa

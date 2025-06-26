from typing import AsyncIterable, Final, Callable

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from dishka import Provider, provide, Scope
from dishka.integrations.aiogram import CONTAINER_NAME
from dishka.integrations.base import wrap_injection
from redis.asyncio import Redis

from src.bot.dispatcher import setup_dispatcher
from src.configuration import Configuration


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_redis(self, conf: Configuration) -> AsyncIterable[Redis]:
        with Redis(
            db=conf.redis.db,
            host=conf.redis.host,
            password=conf.redis.passwd,
            username=conf.redis.username,
            port=conf.redis.port,
            decode_responses=True
        ) as redis:
            yield redis


class FSMStorageProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_storage(self, redis: Redis) -> BaseStorage:
        return RedisStorage(redis=redis)


class ConfigurationProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Configuration:
        return Configuration()


DATA_PARAMETR_POSITION: Final = 3  # self 0, handler 1 , event 2, <data 3>


def inject_md[T](func: Callable[..., T]) -> Callable[..., T]:
    return wrap_injection(
        func=func,
        container_getter=lambda args, _kwargs: args[DATA_PARAMETR_POSITION][
            CONTAINER_NAME
        ],
        is_async=True,
    )


def inject_filter[T](func: Callable[..., T]) -> Callable[..., T]:
    return wrap_injection(
        func=func,
        container_getter=lambda _args, kwargs: kwargs[CONTAINER_NAME],
        is_async=True,
    )

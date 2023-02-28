from typing import Any

from redis.asyncio.client import Redis


class MockedRedis(Redis):
    """Mocked Redis for unittests"""

    data = {}

    async def get(self, name: str) -> str | None:
        return self.data.get(name)

    async def set(self, name: str, value: Any, *_) -> bool | None:
        self.data[name] = value

    async def exists(self, *names: str) -> int:
        return all(name in self.data for name in names)

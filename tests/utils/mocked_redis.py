"""Mocked Redis."""
from typing import Any

from redis.asyncio.client import Redis


class MockedRedis(Redis):
    """Mocked Redis for unittests."""

    data = {}

    async def get(self, name: str) -> str | None:
        """Get value from mocked storage."""
        return self.data.get(name)

    async def set(self, name: str, value: Any, *_) -> bool | None:
        """Set key-value pair in mocked storage."""
        self.data[name] = value
        return True

    async def exists(self, name: str) -> int:
        """Check if keys are exists in mocked storage."""
        return name in self.data

# core/cache/cache.py
from typing import Optional, Any, Dict
from redis import asyncio as aioredis
from core.config import core_settings


class Cache:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)
        self.default_ttl = core_settings.cache.default_ttl

    async def get_value(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def set_value(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        expiry = ttl if ttl is not None else self.default_ttl
        await self.redis.set(key, value, ex=expiry)

    async def get_dict(self, key: str) -> Optional[Dict[str, Any]]:
        import json

        cached_value = await self.redis.get(key)
        if cached_value:
            return json.loads(cached_value)
        return None

    async def set_dict(
        self, key: str, value: Dict[str, Any], ttl: Optional[int] = None
    ) -> None:
        import json

        expiry = ttl if ttl is not None else self.default_ttl
        await self.redis.set(key, json.dumps(value), ex=expiry)

    async def invalidate_key(self, key: str) -> None:

        await self.redis.delete(key)

    async def close(self):
        await self.redis.aclose()


cache = Cache(core_settings.redis.redis_url)

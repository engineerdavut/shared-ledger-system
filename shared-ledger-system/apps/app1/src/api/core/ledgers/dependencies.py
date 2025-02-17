# apps/app1/src/api/core/ledgers/dependencies.py
from fastapi import HTTPException, Depends, Request
from redis import asyncio as aioredis
from core.auth.service import get_current_user
from core.config import core_settings


async def get_redis_pool():
    redis = aioredis.from_url(core_settings.redis.redis_url, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.aclose()


async def rate_limit(
    request: Request,
    user=Depends(get_current_user),
    redis: aioredis.Redis = Depends(get_redis_pool),
):
    client_host = request.client.host if request.client else "unknown"
    endpoint_path = request.url.path
    key = f"ratelimit:{client_host}:{endpoint_path}"
    requests = await redis.get(key)

    rate_limit_requests = core_settings.rate_limit.requests_per_minute
    rate_limit_window = core_settings.rate_limit.window_seconds

    if requests and int(requests) >= rate_limit_requests:
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
        )

    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, rate_limit_window)
    await pipe.execute()

# tests/core/cache/test_cache.py
import pytest
import pytest_asyncio
from core.cache import cache
import asyncio
from core.config import core_settings


@pytest_asyncio.fixture(scope="function")
async def test_cache_fixture():
    from core.cache.cache import Cache

    test_cache = Cache(core_settings.redis.redis_url)
    await test_cache.redis.flushdb()
    yield test_cache
    await test_cache.redis.flushdb()
    await test_cache.redis.aclose()


@pytest.mark.asyncio
async def test_cache_set_get_value(test_cache_fixture: cache):
    key = "test_key_value"
    value = "test_value"
    await test_cache_fixture.set_value(key, value)
    cached_value = await test_cache_fixture.get_value(key)
    assert cached_value == value


@pytest.mark.asyncio
async def test_cache_get_value_not_found(test_cache_fixture: cache):
    key = "non_existent_key_value"
    value = await test_cache_fixture.get_value(key)
    assert value is None


@pytest.mark.asyncio
async def test_cache_set_get_dict(test_cache_fixture: cache):
    key = "test_key_dict"
    value = {"name": "Test Item", "count": 10}
    await test_cache_fixture.set_dict(key, value)
    cached_value = await test_cache_fixture.get_dict(key)
    assert cached_value == value


@pytest.mark.asyncio
async def test_cache_get_dict_not_found(test_cache_fixture: cache):
    key = "non_existent_key_dict"
    value = await test_cache_fixture.get_dict(key)
    assert value is None


@pytest.mark.asyncio
async def test_cache_set_value_with_ttl(test_cache_fixture: cache):
    key = "ttl_key_value"
    value = "ttl_value"
    await test_cache_fixture.set_value(key, value, ttl=1)
    assert await test_cache_fixture.get_value(key) == value
    await asyncio.sleep(2)
    assert await test_cache_fixture.get_value(key) is None


@pytest.mark.asyncio
async def test_cache_set_dict_with_ttl(test_cache_fixture: cache):
    key = "ttl_key_dict"
    value = {"name": "TTL Item", "data": "expires"}
    await test_cache_fixture.set_dict(key, value, ttl=1)
    assert await test_cache_fixture.get_dict(key) == value
    await asyncio.sleep(2)
    assert await test_cache_fixture.get_dict(key) is None


@pytest.mark.asyncio
async def test_cache_invalidate_value(test_cache_fixture: cache):
    key = "invalidate_key_value"
    value = "invalidate_value"
    await test_cache_fixture.set_value(key, value)
    assert await test_cache_fixture.get_value(key) == value
    await test_cache_fixture.invalidate_key(key)
    assert await test_cache_fixture.get_value(key) is None


@pytest.mark.asyncio
async def test_cache_invalidate_dict(test_cache_fixture: cache):
    key = "invalidate_key_dict"
    value = {"name": "Invalidate Item", "type": "dict"}
    await test_cache_fixture.set_dict(key, value)
    assert await test_cache_fixture.get_dict(key) == value
    await test_cache_fixture.invalidate_key(key)
    assert await test_cache_fixture.get_dict(key) is None

# tests/apps/app1/test_rate_limit.py
import pytest
import asyncio
from httpx import AsyncClient
from tests.apps.app1.test_auth import get_access_token_for_test_user
import uuid
from core.auth.models import User
from redis import asyncio as aioredis


@pytest.mark.asyncio
async def test_rate_limiting(client: AsyncClient, db_test_user: User):
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint_url = "/ledger/"

    rate_limited = False
    for _ in range(201):
        response = await client.post(
            endpoint_url,
            json={
                "operation": "CREDIT_ADD",
                "amount": 1,
                "owner_id": "test_user",
                "nonce": str(uuid.uuid4()),
            },
            headers=headers,
        )
        if response.status_code == 429:
            rate_limited = True
            break
        await asyncio.sleep(0.01)

    assert rate_limited, "Rate limit was not applied. Expected 429 status code."
    assert response.status_code == 429

    await asyncio.sleep(121)
    response_after_reset = await client.post(
        endpoint_url,
        json={
            "operation": "CREDIT_ADD",
            "amount": 1,
            "owner_id": "test_user",
            "nonce": str(uuid.uuid4()),
        },
        headers=headers,
    )
    assert response_after_reset.status_code == 200

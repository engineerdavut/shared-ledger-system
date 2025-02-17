# tests/apps/app1/test_api.py
import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.apps.app1.test_auth import get_access_token_for_test_user
from core.auth.models import User
from redis import asyncio as aioredis


@pytest.mark.asyncio
async def test_create_ledger_entry(
    client: AsyncClient, async_session: AsyncSession, db_test_user: User
):
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}
    test_nonce = str(uuid.uuid4())
    payload = {
        "operation": "CREDIT_ADD",
        "amount": 10,
        "owner_id": "test_user",
        "nonce": test_nonce,
    }
    response = await client.post("/ledger/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_duplicate_transaction(
    client: AsyncClient, async_session: AsyncSession, db_test_user: User
):
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}
    test_nonce = str(uuid.uuid4())
    payload = {
        "operation": "CREDIT_ADD",
        "amount": 10,
        "owner_id": "test_user",
        "nonce": test_nonce,
    }

    response1 = await client.post("/ledger/", json=payload, headers=headers)
    assert response1.status_code == 200

    response2 = await client.post("/ledger/", json=payload, headers=headers)
    assert response2.status_code == 409


@pytest.mark.asyncio
async def test_insufficient_balance_api(
    client: AsyncClient, async_session: AsyncSession, db_test_user: User
):
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "operation": "CREDIT_SPEND",
        "amount": -1,
        "owner_id": "test_user2",
        "nonce": str(uuid.uuid4()),
    }
    response = await client.post("/ledger/", json=payload, headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_invalid_operation_api(
    client: AsyncClient, async_session: AsyncSession, db_test_user: User
):
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "operation": "INVALID_OPERATION",
        "amount": 10,
        "owner_id": "test_user",
        "nonce": str(uuid.uuid4()),
    }
    response = await client.post("/ledger/", json=payload, headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_balance_api(
    client: AsyncClient, async_session: AsyncSession, db_test_user: User
):
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/ledger/test_user", headers=headers)
    assert response.status_code == 200
    assert "balance" in response.json()

# tests/apps/app1/test_api.py
import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_ledger_entry(client: AsyncClient, async_session: AsyncSession):
    test_nonce = str(uuid.uuid4())
    payload = {
        "operation": "CREDIT_ADD",
        "amount": 10,
        "owner_id": "test_user",
        "nonce": test_nonce
    }
    response = await client.post("/ledger/", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_duplicate_transaction(client: AsyncClient, async_session: AsyncSession):
    test_nonce = str(uuid.uuid4())
    payload = {
        "operation": "CREDIT_ADD",
        "amount": 10,
        "owner_id": "test_user",
        "nonce": test_nonce
    }

    response1 = await client.post("/ledger/", json=payload)
    assert response1.status_code == 200

    response2 = await client.post("/ledger/", json=payload)
    assert response2.status_code == 409

# Yeni Testler:
@pytest.mark.asyncio
async def test_insufficient_balance_api(client: AsyncClient, async_session: AsyncSession):
    payload = {
        "operation": "CREDIT_SPEND",
        "amount": -1,  # Yetersiz bakiye
        "owner_id": "test_user2",
        "nonce": str(uuid.uuid4())
    }
    response = await client.post("/ledger/", json=payload)
    assert response.status_code == 400  # Beklenen hata kodu

@pytest.mark.asyncio
async def test_invalid_operation_api(client: AsyncClient, async_session: AsyncSession):
    payload = {
        "operation": "INVALID_OPERATION",
        "amount": 10,
        "owner_id": "test_user",
        "nonce": str(uuid.uuid4())
    }
    response = await client.post("/ledger/", json=payload)
    assert response.status_code == 400  # Beklenen hata kodu

@pytest.mark.asyncio
async def test_get_balance_api(client: AsyncClient, async_session: AsyncSession):
  # Add some initial entries (optional)
    response = await client.get("/ledger/test_user")
    assert response.status_code == 200
    assert "balance" in response.json()
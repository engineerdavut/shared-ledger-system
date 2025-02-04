# tests/apps/app1/test_api.py
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_get_balance():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/ledger/test_user")
        assert response.status_code == 200
        data = response.json()
        assert "balance" in data
        assert "owner_id" in data
        assert data["owner_id"] == "test_user"

@pytest.mark.asyncio
async def test_create_ledger_entry():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "operation": "CREDIT_ADD",
            "amount": 10,
            "owner_id": "test_user",
            "nonce": "test_nonce_1"
        }
        response = await client.post("/ledger/", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_duplicate_transaction():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "operation": "CREDIT_ADD",
            "amount": 10,
            "owner_id": "test_user",
            "nonce": "test_nonce_2"
        }
        # İlk işlem
        response1 = await client.post("/ledger/", json=payload)
        assert response1.status_code == 200
        
        # Aynı nonce ile ikinci işlem
        response2 = await client.post("/ledger/", json=payload)
        assert response2.status_code == 409  # Conflict
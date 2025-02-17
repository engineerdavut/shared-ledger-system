# tests/apps/app1/test_auth.py
import pytest
from httpx import AsyncClient
from core.auth.service import create_access_token
from core.auth.models import User
from redis import asyncio as aioredis
import asyncio


async def get_access_token_for_test_user(db_test_user: User) -> str:
    token_payload = {"sub": db_test_user.username, "user_id": str(db_test_user.id)}
    token = create_access_token(data=token_payload)
    return token


@pytest.mark.asyncio
async def test_auth_valid_token(client: AsyncClient, db_test_user: User):
    access_token = await get_access_token_for_test_user(db_test_user)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/ledger/test_user", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_auth_invalid_token(client: AsyncClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/ledger/test_user", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_no_token(client: AsyncClient):
    response = await client.get("/ledger/test_user")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_login_endpoint(client: AsyncClient, db_test_user: User):
    login_data = {"username": db_test_user.username, "password": "test_password"}
    response = await client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_auth_register_endpoint(client: AsyncClient):
    await asyncio.sleep(0.1)
    register_data = {
        "username": "newuser",
        "password": "newpassword",
        "email": "newuser@example.com",
    }
    response = await client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert "id" in response.json()

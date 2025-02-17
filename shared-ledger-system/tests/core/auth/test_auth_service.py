# tests/core/auth/test_auth_service.py
import pytest
from core.auth.service import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    get_user_by_username,
)
from core.auth.models import User

from fastapi import HTTPException

from unittest.mock import AsyncMock
from core.auth.schemas import TokenPayload
from sqlalchemy.ext.asyncio import AsyncSession


def test_password_hashing_and_verification():
    password = "test_password"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("wrong_password", hashed_password)


def test_create_access_token():
    user = User(id=1, username="testuser", hashed_password="hashed_pw")
    token_payload_data = {"sub": user.username, "user_id": str(user.id)}
    token = create_access_token(data=TokenPayload(**token_payload_data).model_dump())
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_get_current_user_valid_token(
    db_test_user: User, async_session: AsyncSession
):
    token_payload = {"sub": db_test_user.username, "user_id": db_test_user.id}
    token = create_access_token(data=token_payload)
    user = await get_current_user(token=token, session=async_session)
    assert user.id == db_test_user.id


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    mock_session = AsyncMock(AsyncSession)
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="invalid_token", session=mock_session)
    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_user_by_username_db(async_session: AsyncSession):
    test_user = User(
        username="db_testuser", hashed_password=get_password_hash("test_password")
    )
    async_session.add(test_user)
    await async_session.commit()
    retrieved_user = await get_user_by_username(async_session, username="db_testuser")
    assert retrieved_user is not None
    assert retrieved_user.username == "db_testuser"

# core/auth/service.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.db.base import get_session
from core.auth import models, schemas
from core.config import core_settings
from core.cache import cache
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

auth_cache = cache


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(minutes=core_settings.jwt.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, core_settings.jwt.secret_key, algorithm=core_settings.jwt.algorithm
    )
    return encoded_jwt


async def get_user_by_username(
    session: AsyncSession, username: str
) -> Optional[models.User]:
    result = await session.execute(
        select(models.User).where(models.User.username == username)
    )
    return result.scalar_one_or_none()


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> Optional[models.User]:
    user = await get_user_by_username(session, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            core_settings.jwt.secret_key,
            algorithms=[core_settings.jwt.algorithm],
        )
        username: str = payload.get("sub")
        user_id_str: str = payload.get("user_id")
        if username is None or user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
        token_data = schemas.TokenPayload(sub=username, user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = await get_user_from_cache_or_db(
        session, username=token_data.sub, user_id=token_data.user_id
    )
    if user is None:
        raise credentials_exception
    return user


async def get_user_from_cache_or_db(
    session: AsyncSession, username: str, user_id: int
) -> Optional[models.User]:
    cached_user_dict = await auth_cache.get_dict(f"user:{user_id}")
    if cached_user_dict:
        return models.User(**cached_user_dict)
    user = await get_user_by_username(session, username=username)
    if user:
        user_schema = schemas.UserSchema.model_validate(user)
        await auth_cache.set_dict(f"user:{user_id}", user_schema.model_dump(), ttl=600)
    return user


async def create_user(
    session: AsyncSession, user_create: schemas.UserCreate
) -> models.User:
    hashed_password = get_password_hash(user_create.password)
    db_user = models.User(
        username=user_create.username,
        hashed_password=hashed_password,
        email=user_create.email,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

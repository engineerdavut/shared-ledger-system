# tests/conftest.py
import os
import sys
import asyncio
import pytest
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pytest_asyncio
from alembic.config import Config
from alembic import command
from datetime import datetime, timezone
import uuid
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from redis import asyncio as aioredis

load_dotenv(".env.test")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.config import core_settings
from core.auth.models import User
from core.auth.service import get_password_hash
from core.db.base import Base


DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "test_db")
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
        asyncio.set_event_loop(None)


@pytest_asyncio.fixture(scope="session")
async def test_database():
    await create_test_database()
    yield
    await drop_test_database()


async def create_test_database():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database="postgres",
    )
    try:
        exists = await conn.fetchval(
            f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')
    finally:
        await conn.close()


async def drop_test_database():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database="postgres",
    )
    try:
        await conn.execute(
            f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{TEST_DB_NAME}' AND pid <> pg_backend_pid();
        """
        )
        await asyncio.sleep(1)
        await conn.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"')
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_test_database(async_engine):
    print("Using TEST_DATABASE_URL =", TEST_DATABASE_URL)
    await create_test_database()

    alembic_cfg = Config("core/db/migrations/alembic_test.ini")
    alembic_cfg.set_main_option("script_location", "core/db/migrations/alembic")
    command.upgrade(alembic_cfg, "head")

    yield

    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database="postgres",
    )
    try:
        await conn.execute(
            f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{TEST_DB_NAME}' AND pid <> pg_backend_pid();
        """
        )
    finally:
        await conn.close()

    command.downgrade(alembic_cfg, "base")
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()
    await asyncio.sleep(0.5)
    await drop_test_database()


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL, pool_size=20, max_overflow=0, pool_pre_ping=True
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    Session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession, autoflush=False
    )
    async with Session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest_asyncio.fixture
async def client(async_engine):
    from apps.app1.src.main import app
    from core.db.base import get_session
    from httpx import AsyncClient
    from httpx._transports.asgi import ASGITransport
    from core.config import core_settings

    async def override_get_session():
        Session = sessionmaker(
            async_engine, expire_on_commit=False, class_=AsyncSession
        )
        async with Session() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    redis_instance = aioredis.from_url(
        core_settings.redis.redis_url, decode_responses=True
    )
    app.state.redis = redis_instance
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            ac.app = app
            yield ac
    finally:
        app.dependency_overrides.clear()
        await redis_instance.aclose()
        await asyncio.sleep(0.1)


@pytest_asyncio.fixture
async def db_test_user(async_session: AsyncSession) -> User:
    user = User(
        username=f"testuser_{uuid.uuid4()}",
        hashed_password=get_password_hash("test_password"),
        email=f"testuser_{uuid.uuid4()}@example.com",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user

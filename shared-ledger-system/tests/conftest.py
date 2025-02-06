# tests/conftest.py
# tests/conftest.py
import os
import sys
import asyncio
import pytest
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Proje kök dizinini sys.path'e ekleyin (gerekirse)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.db.base import Base

# Ortam değişkenlerinden bağlantı bilgilerini oku
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "test_db")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}")

# --- Event loop fixture (pytest_asyncio varsayılanını kullanmaya da izin verebilirsiniz) ---
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# --- Test veritabanını oluştur ve testler bitince sil ---
async def create_test_database():
    admin_conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database="postgres"
    )
    try:
        exists = await admin_conn.fetchval("SELECT 1 FROM pg_database WHERE datname=$1", TEST_DB_NAME)
        if not exists:
            await admin_conn.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')
    finally:
        await admin_conn.close()

async def drop_test_database():
    admin_conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database="postgres"
    )
    try:
        await admin_conn.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"')
    finally:
        await admin_conn.close()

@pytest.fixture(scope="session", autouse=True)
async def initialize_test_database():
    # Test başlamadan önce veritabanını oluştur
    await create_test_database()
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Testler bittikten sonra tabloları sil
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    # Test veritabanını sil
    await drop_test_database()

@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

# Her test için yeni bir session (her test ayrı session, transaction rollback ile izolasyon)
@pytest.fixture
async def async_session(async_engine):
    async_session_factory = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_factory() as session:
        yield session
        await session.rollback()

# ASGI uygulamasını test etmek için asenkron HTTP client (httpx)
@pytest.fixture
async def client():
    from apps.app1.src.main import app
    from httpx import AsyncClient
    from httpx._transports.asgi import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

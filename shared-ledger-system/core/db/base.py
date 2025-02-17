# core/db/base.py
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from core.config import core_settings

load_dotenv()

Base = declarative_base()

DATABASE_URL = core_settings.database.database_url

async_engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

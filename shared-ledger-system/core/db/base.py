# core/db/base.py
# core/db/base.py
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# .env'den DATABASE_URL'yi oku
DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL'nin "postgresql+asyncpg://" ile başladığından emin ol



async_engine = create_async_engine(DATABASE_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
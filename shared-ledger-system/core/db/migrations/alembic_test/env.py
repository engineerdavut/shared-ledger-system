# core/db/migrations/alembic_test/env.py
import os
import sys
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
import asyncio
import nest_asyncio

nest_asyncio.apply()

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from alembic import context
from dotenv import load_dotenv

load_dotenv()

from core.db.base import Base
from core.auth.models import User
from core.ledgers.models import LedgerEntry

target_metadata = Base.metadata

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import psycopg2
from sqlalchemy.engine.url import make_url


def ensure_db_exists(db_url: str):
    url_obj = make_url(db_url)
    db_name = url_obj.database

    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "12345")
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")

    conn = psycopg2.connect(
        dbname="postgres",
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    conn.autocommit = True

    with conn.cursor() as cursor:
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            cursor.execute(f'CREATE DATABASE "{db_name}"')
    conn.close()


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    full_url = config.get_main_option("sqlalchemy.url")
    ensure_db_exists(full_url)
    connectable: AsyncEngine = create_async_engine(full_url)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

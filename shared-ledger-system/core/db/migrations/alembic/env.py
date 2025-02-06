#alembic/env.py
import os
import sys
from logging.config import fileConfig

# Proje kök dizininin yolunu sys.path'e ekleyin
# env.py, core/db/migrations/alembic/ içinde olduğundan, üç seviye yukarıya çıkıyoruz:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv  # dotenv'i import et

load_dotenv() # .env dosyasını yükle


# Alembic konfigürasyon nesnesini alıyoruz
config = context.config

# .env dosyasından veritabanı URL'sini al ve Alembic konfigürasyonuna ekle
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


# Log yapılandırması
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Core modülündeki Base'i mutlak olarak import edin
from core.db.base import Base
from core.ledgers import models
target_metadata = Base.metadata

import psycopg2
from sqlalchemy.engine.url import make_url
# from sqlalchemy import create_engine # buna gerek yok

def ensure_db_exists(db_url: str):
    """Veritabanını kontrol edip, eğer yoksa oluşturur."""
    url_obj = make_url(db_url)
    db_name = url_obj.database

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
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

def run_migrations_online() -> None:
    full_url = config.get_main_option("sqlalchemy.url")
    ensure_db_exists(full_url)
    # connectable = engine_from_config( # engine_from_config yerine direkt create_async_engine kullan
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    connectable = create_async_engine(full_url) # .env'den okunan URL ile engine oluştur
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
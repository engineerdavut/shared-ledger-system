# core/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Dict


class DatabaseSettings(BaseSettings):
    database_url: str = os.environ.get("DATABASE_URL")
    database_pool_size: int = 5

    @field_validator("database_url")
    def validate_database_url(cls, v):
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError("DATABASE_URL must start with 'postgresql+asyncpg://'")
        return v

    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class RedisSettings(BaseSettings):
    redis_url: str = os.environ.get("REDIS_URL", "redis://redis:6379")
    model_config = SettingsConfigDict(env_prefix="REDIS_")


class LoggingSettings(BaseSettings):
    log_level: str = os.environ.get("LOGGING_LEVEL", "INFO").upper()
    log_file: str = "ledger_service.log"

    @field_validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v not in valid_levels:
            raise ValueError(f"LOGGING_LEVEL must be one of {valid_levels}")
        return v

    model_config = SettingsConfigDict(env_prefix="LOGGING_")


class PrometheusSettings(BaseSettings):
    prometheus_enabled: bool = True
    model_config = SettingsConfigDict(env_prefix="PROMETHEUS_")


class JWTSettings(BaseSettings):
    secret_key: str = os.environ.get("SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(
        os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    model_config = SettingsConfigDict(env_prefix="JWT_")


class RateLimitSettings(BaseSettings):

    requests_per_minute: int = 100
    window_seconds: int = 60
    model_config = SettingsConfigDict(env_prefix="RATE_LIMIT_")


class CacheSettings(BaseSettings):
    redis_url: str = os.environ.get("REDIS_URL", "redis://redis:6379")
    default_ttl: int = 360


class LedgerSettings(BaseSettings):
    operation_config: Dict[str, int] = {
        "DAILY_REWARD": 1,
        "SIGNUP_CREDIT": 3,
        "CREDIT_SPEND": -1,
        "CREDIT_ADD": 10,
    }


class Settings(BaseSettings):
    app_name: str = "Shared Ledger System"
    debug: bool = False

    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    logging: LoggingSettings = LoggingSettings()
    prometheus: PrometheusSettings = PrometheusSettings()
    jwt: JWTSettings = JWTSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    cache: CacheSettings = CacheSettings()
    ledger: LedgerSettings = LedgerSettings()

    model_config = SettingsConfigDict(
        env_file=".env" if os.environ.get("ENVIRONMENT") != "test" else ".env.test",
        env_file_encoding="utf-8",
        extra="ignore",
    )


core_settings = Settings()

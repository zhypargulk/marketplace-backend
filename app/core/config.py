from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60

    admin_email: str
    admin_password: str

    minio_endpoint: str
    minio_access_key: str = Field(validation_alias=AliasChoices("MINIO_ROOT_USER", "APP_MINIO_ACCESS_KEY"))
    minio_secret_key: str = Field(validation_alias=AliasChoices("MINIO_ROOT_PASSWORD", "APP_MINIO_SECRET_KEY"))
    minio_secure: bool = False
    minio_bucket_products: str = "products"


@lru_cache
def get_settings() -> Settings:
    return Settings()


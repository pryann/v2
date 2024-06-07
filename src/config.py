from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str
    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_LOG_LEVEL: str
    SERVER_TTL: int
    SSL_KEYFILE: str
    SSL_CERTFILE: str
    DATABASE_ENGINE: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    CORS_ORIGINS: str
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def DATABASE_URL(self) -> str:
        async_postfix = "+asyncpg" if self.DATABASE_ENGINE == "postgresql" else ""
        return f"{self.DATABASE_ENGINE}{async_postfix}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()

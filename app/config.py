from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME")
    APP_ENV: str = Field(env="APP_ENV")
    SERVER_HOST: str = Field(env="SERVER_HOST")
    SERVER_PORT: int = Field(env="SERVER_PORT")
    SERVER_LOG_LEVEL: str = Field(env="SERVER_LOG_LEVEL")
    MYSQL_HOST: str = Field(env="MYSQL_HOST")
    MYSQL_PORT: int = Field(env="MYSQL_PORT")
    MYSQL_DATABASE: str = Field(env="MYSQL_DATABASE")
    MYSQL_USER: str = Field(env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(env="MYSQL_PASSWORD")
    MYSQL_ROOT_PASSWORD: str = Field(env="MYSQL_ROOT_PASSWORD")
    CORS_ORIGINS: str = Field(env="CORS_ORIGINS")

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def MYSQL_DATABASE_URL(self) -> str:
        return f"mysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()

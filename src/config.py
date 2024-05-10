from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MYSQL_HOST: str = Field(env="MYSQL_HOST")
    MYSQL_PORT: int = Field(env="MYSQL_PORT")
    MYSQL_DATABASE: str = Field(env="MYSQL_DATABASE")
    MYSQL_USER: str = Field(env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(env="MYSQL_PASSWORD")
    MYSQL_ROOT_PASSWORD: str = Field(env="MYSQL_ROOT_PASSWORD")
    MYSQL_DATABASE_URL: str = Field(env="MYSQL_DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()

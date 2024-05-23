from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


# PROJECT_NAME: str = Field(env="PROJECT_NAME")
# APP_ENV: str = Field(env="APP_ENV")
# SERVER_HOST: str = Field(env="SERVER_HOST")
# SERVER_PORT: int = Field(env="SERVER_PORT")
# SERVER_LOG_LEVEL: str = Field(env="SERVER_LOG_LEVEL")
# MYSQL_HOST: str = Field(env="MYSQL_HOST")
# MYSQL_PORT: int = Field(env="MYSQL_PORT")
# MYSQL_DATABASE: str = Field(env="MYSQL_DATABASE")
# MYSQL_USER: str = Field(env="MYSQL_USER")
# MYSQL_PASSWORD: str = Field(env="MYSQL_PASSWORD")
# MYSQL_ROOT_PASSWORD: str = Field(env="MYSQL_ROOT_PASSWORD")
# CORS_ORIGINS: str = Field(env="CORS_ORIGINS")
# ACCESS_TOKEN_SECRET_KEY: str = Field(env="ACCESS_TOKEN_SECRET_KEY")
# ACCESS_TOKEN_ALGORITHM: str = Field(env="ACCESS_TOKEN_ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES: str = Field(env="ACCESS_TOKEN_EXPIRE_MINUTE")
# REFRESH_TOKEN_SECRET_KEY: str = Field(env="REFRESH_TOKEN_SECRET_KEY")
# REFRESH_TOKEN_ALGORITHM: str = Field(env="REFRESH_TOKEN_ALGORITHM")
# REFRESH_TOKEN_EXPIRE_MINUTES: str = Field(env="REFRESH_TOKEN_EXPIRE_MINUTES")
class Settings(BaseSettings):
    PROJECT_NAME: str
    APP_ENV: str
    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_LOG_LEVEL: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_ROOT_PASSWORD: str
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
    def MYSQL_DATABASE_URL(self) -> str:
        return f"mysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()

# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DATABASE_MONGO_URL: str
    DATABASE_POSTGRES_URL: str


settings = Settings()  # type: ignore[call-arg]

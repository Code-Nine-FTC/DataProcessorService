# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DATABASE_MONGO_URL: str
    DATABASE_POSTGRES_URL: str
    MQTT_BROKER_HOST: str
    MQTT_BROKER_PORT: int
    MQTT_BROKER_TOPIC: str
    MQTT_BROKER_CLIENT_NAME: str
    MQTT_BROKER_KEEPALIVE: int
    TIME_FOR_SYNC_DATA: int


settings = Settings()  # type: ignore[call-arg]

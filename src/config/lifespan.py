# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from src.config.dependency.mongo_db import DatabaseMongo
from src.config.schedule import ScheduleConfig
from src.config.settings import Settings
from src.services.ingestion.mqtt_consumer import MQTTConsumer
from src.services.processing.sync_postgres import SyncPostgres
from src.utils.common import Singleton


class AppLifecycleManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.mongo_db = DatabaseMongo()
        self.mqtt_consumer = MQTTConsumer()
        self.scheduler = ScheduleConfig()
        self.sync_postgres = SyncPostgres()
        self.settings = Settings()  # type: ignore[call-arg]

    async def start_services(self) -> None:
        self.mongo_db.ping()
        self.mqtt_consumer.start()
        self.scheduler.add_job(
            self.sync_postgres.execute,
            self.settings.TIME_FOR_SYNC_DATA,
            job_id="sync_postgres",
        )

    async def stop_services(self) -> None:
        self.mongo_db.close()
        self.mqtt_consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    try:
        await AppLifecycleManager().start_services()
        yield
    finally:
        await AppLifecycleManager().stop_services()

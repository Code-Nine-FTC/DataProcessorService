# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from src.config.dependency.mongo_db import DatabaseMongo
from src.config.dependency.postgres_db import Database
from src.services.ingestion.mqtt_consumer import MQTTConsumer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    try:
        await Database().ping()
        DatabaseMongo().ping()
        MQTTConsumer().start()
        yield
    finally:
        await Database().close()
        DatabaseMongo().close()
        MQTTConsumer().close()

# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from src.config.dependency.mongo_db import DatabaseMongo
from src.services.ingestion.mqtt_consumer import MQTTConsumer
from src.services.processing.mongo_observer import MongoObserver


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    try:
        DatabaseMongo().ping()
        MQTTConsumer(MongoObserver()).start()
        yield
    finally:
        DatabaseMongo().close()
        MQTTConsumer(MongoObserver()).stop()

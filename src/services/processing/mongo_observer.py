# -*- coding: utf-8 -*-
from typing import Any

from src.services.ingestion.mongo_repository import MongoRepository
from src.utils.common import CombinedMeta, DataObserver
import logging

class MongoObserver(DataObserver, metaclass=CombinedMeta):
    def __init__(self) -> None:
        self.__mongo_repository = MongoRepository()

    def on_data_received(self, data: dict[str, Any]) -> None:
        try:
            self.__mongo_repository.insert_data(data)
        except Exception as e:
            logging.error("Failed to insert data into MongoDB: %s", e)
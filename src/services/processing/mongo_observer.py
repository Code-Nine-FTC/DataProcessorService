# -*- coding: utf-8 -*-
from typing import Any

from src.services.ingestion.mongo_repository import MongoRepository
from src.utils.common import CombinedMeta, DataObserver


class MongoObserver(DataObserver, metaclass=CombinedMeta):
    def __init__(self) -> None:
        self.__mongo_repository = MongoRepository()
        self._buffer: list[dict[str, Any]] = []


    def on_data_received(self, data: dict[str, Any]) -> None:
        self._buffer.append(data)
        if len(self._buffer) >= 500:
            try:
                self.__mongo_repository.insert_batch_data(self._buffer)
                self._buffer.clear()
            except Exception as e:
                raise Exception(f"Error inserting data into MongoDB: {e}") from e
    
    def flush(self) -> None:
        if self._buffer:
            try:
                self.__mongo_repository.insert_batch_data(self._buffer)
                self._buffer.clear()
            except Exception as e:
                raise Exception(f"Error flushing data into MongoDB: {e}") from e

# -*- coding: utf-8 -*-
from typing import Any

from src.config.dependency.mongo_db import DatabaseMongo
from src.utils.common import Singleton


class MongoRepository(metaclass=Singleton):
    def __init__(self) -> None:
        self._database_mongo = DatabaseMongo()
        self._collection_name = "station_data"
        self._collection = self._database_mongo.get_collection(self._collection_name)

    def insert_data(self, data: dict[str, Any]) -> None:
        self._collection.insert_one(data)
        
    def insert_batch_data(self, data_list: list[dict[str, Any]]) -> None:
        if data_list:
            self._collection.insert_many(data_list)

    def get_all_data(self) -> list[dict[str, Any]]:
        return [data for data in self._collection.find()]

    def remove_all_data(self) -> None:
        self._collection.delete_many({})

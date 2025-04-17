# -*- coding: utf-8 -*-
from src.config.dependency.mongo_db import DatabaseMongo
from src.schemas.station import StationData


class MongoRepository:
    def __init__(self) -> None:
        self._database_mongo = DatabaseMongo()
        self._collection_name = "station_data"
        self._collection = self._database_mongo.get_collection(self._collection_name)

    def insert_data(self, data: dict) -> None:
        self._collection.insert_one(data)

    def get_all_data(self) -> list[StationData]:
        return [StationData(**data) for data in self._collection.find()]

    def remove_all_data(self) -> None:
        self._collection.delete_many({})

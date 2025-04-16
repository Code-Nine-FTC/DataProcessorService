# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from src.config.dependency.mongo_db import DatabaseMongo
from src.config.dependency.postgres_db import SessionConnection
from src.services.storage.postgres_storage import PostgresStorage


class MongoObserver:
    def __init__(self, collection_name: str):
        self.mongo_client = DatabaseMongo()
        self.collection = self.mongo_client.get_collection(collection_name)
        self.postgres_storage = PostgresStorage()

    async def observe_changes(self):
        try:
            with self.collection.watch() as stream:
                for change in stream:
                    if change["operationType"] == "insert":
                        document = change["fullDocument"]

                        if not await self._is_processed(document["_id"]):
                            await self._process_data(document)
        except PyMongoError as e:
            print(f"Error observing changes: {e}")
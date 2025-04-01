# -*- coding: utf-8 -*-
from pymongo.database import Collection, Database
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.config.settings import Settings
from src.utils.common import Singleton


class DatabaseMongo(metaclass=Singleton):
    def __init__(self) -> None:
        self._settings: Settings = Settings()  # type: ignore[call-arg]
        self._client: MongoClient = self.create_client()  # type: ignore[no-any-unimported]
        self._db = self.get_database()

    def create_client(self) -> MongoClient:  # type: ignore[no-any-unimported]
        return MongoClient(
            self._settings.DATABASE_MONGO_URL, server_api=ServerApi("1")
        )

    def close(self) -> None:
        self._client.close()

    def ping(self) -> bool:
        try:
            self._client.admin.command("ping")
            print("MongoDB ping successful")
            return True
        except Exception as e:
            raise Exception(f"MongoDB ping failed: {e}") from e

    def get_database(self) -> Database:  # type: ignore[no-any-unimported]
        return self._client["tecsus"]

    def get_collection(self, collection_name: str) -> Collection:  # type: ignore[no-any-unimported]
        return self._db[collection_name]

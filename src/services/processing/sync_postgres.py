# -*- coding: utf-8 -*-

import logging

from src.config.dependency.postgres_db import DatabasePostgres
from src.services.ingestion.mongo_repository import MongoRepository
from src.services.storage.storage import PostgresStorage


class SyncPostgres:
    def __init__(self) -> None:
        self._mongo_repository = MongoRepository()

    async def execute(self) -> None:
        try:
            datas_mongo = self._mongo_repository.get_all_data()
            if len(datas_mongo) == 0:
                logging.info("No data to sync")
                return
            async with DatabasePostgres().session as session:
                postgres_storage = PostgresStorage(session)
                await postgres_storage.execute(datas_mongo)
            self._mongo_repository.remove_all_data()
            logging.info("Data synced successfully")
        except Exception as e:
            logging.error(f"Error syncing data: {e}")

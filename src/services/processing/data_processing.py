# -*- coding: utf-8 -*-
from src.services.ingestion.mongo_repository import MongoRepository
from src.services.storage.postgres_storage import PostgresStorage
from src.config.dependency.postgres_db import SessionConnection
from src.schemas.station import StationData

class DataProcessing:
    def __init__(self, mongo_collection: str):
        self.mongo_repo = MongoRepository(mongo_collection)

    print("DataProcessing initialized")

async def process_data(self):
    mongo_data = self.mongo_repo.get_all_data()

    async with SessionConnection.session() as session:
        detect_types = await postgres_storage.get_active_detect_types(session)
        transformed_data = []

        for document in mongo_data:
            sensor_uid = int(document["sensor_id"])
            timestamp = int(document["timestamp"])

            for detect_type in detect_types:
                if detect_type in document:
                    value = document[detect_type]

                    data = StationData(
                        uid=sensor_uid,
                        value=value,
                        create_date=timestamp,
                        parameter_type=[detect_type],
                        mongo_id=str(document["_id"])
                    )
                    transformed_data.append(data)

        postgres_storage = PostgresStorage(session, transformed_data)
        await postgres_storage.execute()
        print(f"Inseridos {len(transformed_data)} registros no Postgres.")


class SyncDataProcessing:
    def __init__(self):
        pass

    def _format_data(self):
        return

    def _build_data(self):
        return

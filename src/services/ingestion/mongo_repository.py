# -*- coding: utf-8 -*-
from src.config.dependency.mongo_db import DatabaseMongo


class MongoRepository:
    def __init__(self, collection_name: str):
        self.database_mongo = DatabaseMongo()
        self.collection = self.database_mongo.get_collection(collection_name)

    def insert_data(self, data: dict):
        print(f"Inserindo dados na coleção '{self.collection.name}': {data}")
        self.collection.insert_one(data)
        print(f"Dados inseridos com sucesso na coleção '{self.collection.name}'.")

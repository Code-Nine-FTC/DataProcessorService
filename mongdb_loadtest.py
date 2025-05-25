import os
import time

from pymongo import MongoClient

client = MongoClient(os.getenv("DATABASE_MONGO_URL"))
collection = client.db.station_data

start = time.time()

for i in range(10000):
    doc = {"station_id": i, "value": 42, "timestamp": time.time()}
    collection.insert_one(doc)

end = time.time()
print(f"Tempo total: {end - start:.2f} segundos")

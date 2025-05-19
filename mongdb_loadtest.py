from pymongo import MongoClient
import time

client = MongoClient("mongodb+srv://ninecodek9:hC5EPmsZw2VoJS2S@cluster0.sfjpedo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
collection = client.db.station_data

start = time.time()

for i in range(10000):
    doc = {"station_id": i, "value": 42, "timestamp": time.time()}
    collection.insert_one(doc)

end = time.time()
print(f"Tempo total: {end - start:.2f} segundos")
# -*- coding: utf-8 -*-
import json

from src.config.dependency.mqtt_client_connection import MQTTClientConnection
from src.config.settings import Settings
from src.services.ingestion.mongo_repository import MongoRepository


class MQTTConsumer:
    def __init__(self) -> None:
        self.mongo_repository = MongoRepository("station_data")
        self.mqtt_client_connection = MQTTClientConnection()
        self.mqtt_client_connection.mqtt_client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        print("Message received from MQTT:", msg.payload.decode())
        try:
            payload = json.loads(msg.payload.decode())
            print("Payload:", payload)
            self.mongo_repository.insert_data(payload)
            print("Data successfully inserted into MongoDB")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"MQTT message failed: {e}")

    def start(self) -> None:
        self.mqtt_client_connection.connect()
        self.mqtt_client_connection.mqtt_client.subscribe(
            Settings().MQTT_BROKER_TOPIC
        )
        self.mqtt_client_connection.start_loop()

    def stop(self) -> None:
        self.mqtt_client_connection.stop_loop()
        self.mqtt_client_connection.disconnect()

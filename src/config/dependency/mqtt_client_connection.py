# -*- coding: utf-8 -*-
import json

from paho.mqtt.client import Client

from src.config.broker import MQTT_BROKER_CONFIG
from src.services.ingestion.mongo_repository import MongoRepository


class MQTTHandler:
    def __init__(self) -> None:
        self.mongo_repository = MongoRepository("station_data")
        self.mqtt_client = Client(client_id=MQTT_BROKER_CONFIG["CLIENT_NAME"])
        self.mqtt_client.on_message = self.on_message
        self._is_connected = False

    def on_message(self, client, userdata, msg):
        print("Message received from MQTT:", msg.payload.decode())
        try:
            payload = json.loads(msg.payload.decode())
            print("Payload decodificado:", payload)
            self.mongo_repository.insert_data(payload)
            print("Data successfully inserted into MongoDB")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"MQTT message failed: {e}")

    def start(self) -> None:
        try:
            self.mqtt_client.connect(
                MQTT_BROKER_CONFIG["HOST"],
                MQTT_BROKER_CONFIG["PORT"],
                keepalive=MQTT_BROKER_CONFIG["KEEPALIVE"],
            )
            self.mqtt_client.subscribe(MQTT_BROKER_CONFIG["TOPIC"])
            self.mqtt_client.loop_start()
            self._is_connected = True
            print(f"MQTT Connected on: {MQTT_BROKER_CONFIG['HOST']}")
        except Exception as e:
            print(f"MQTT Connection failed: {e}")
            self._is_connected = False

    async def ping(self) -> bool:
        if self.mqtt_client.is_connected():
            print("MQTT ping successful")
            return True
        print("MQTT ping failed")
        return False

    def close(self) -> None:
        if self._is_connected:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self._is_connected = False

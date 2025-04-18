# -*- coding: utf-8 -*-
import json

from src.config.dependency.mqtt_client_connection import MQTTClientConnection
from src.config.settings import Settings
from src.services.processing.mongo_observer import MongoObserver
from src.utils.common import Singleton


class MQTTConsumer(metaclass=Singleton):
    def __init__(self) -> None:
        self.__mqtt_client_connection = MQTTClientConnection()
        self.__mqtt_client_connection.mqtt_client.on_message = self.on_message
        self.__observer = MongoObserver()

    def on_message(self, client: object, userdata: object, msg: object) -> None:
        print("Message received from MQTT:", msg.payload.decode())
        try:
            payload = json.loads(msg.payload.decode())
            print("Payload:", payload)
            self.__observer.on_data_received(payload)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self) -> None:
        self.__mqtt_client_connection.connect()
        self.__mqtt_client_connection.mqtt_client.subscribe(
            Settings().MQTT_BROKER_TOPIC
        )
        self.__mqtt_client_connection.start_loop()

    def stop(self) -> None:
        self.__mqtt_client_connection.stop_loop()
        self.__mqtt_client_connection.disconnect()

# -*- coding: utf-8 -*-
from paho.mqtt.client import Client

from src.config.settings import Settings
from src.utils.common import Singleton


class MQTTClientConnection(metaclass=Singleton):
    def __init__(self) -> None:
        self._settings = Settings()  # type: ignore[call-arg]
        self.mqtt_client = Client(client_id=self._settings.MQTT_BROKER_CLIENT_NAME)
        self._is_connected = False

    def connect(self) -> None:
        try:
            self.mqtt_client.connect(
                self._settings.MQTT_BROKER_HOST,
                self._settings.MQTT_BROKER_PORT,
                keepalive=self._settings.MQTT_BROKER_KEEPALIVE,
            )
            self._is_connected = True
            print(f"MQTT Connected on: {self._settings.MQTT_BROKER_HOST}")
        except Exception as e:
            print(f"MQTT Connection failed: {e}")
            self._is_connected = False

    def start_loop(self) -> None:
        if self._is_connected:
            self.mqtt_client.loop_start()

    def stop_loop(self) -> None:
        if self._is_connected:
            self.mqtt_client.loop_stop()

    def disconnect(self) -> None:
        if self._is_connected:
            self.mqtt_client.disconnect()
            self._is_connected = False

    def is_connected(self) -> bool:
        return self.mqtt_client.is_connected()

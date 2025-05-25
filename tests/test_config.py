from typing import Generator, Tuple
from unittest.mock import Mock, patch

import pytest

from src.config.dependency.mqtt_client_connection import MQTTClientConnection


@pytest.fixture
def mqtt_client_conn() -> Generator[Tuple[MQTTClientConnection, Mock], None, None]:
    with (
        patch(
            "src.config.dependency.mqtt_client_connection.Settings"
        ) as MockSettings,
        patch("src.config.dependency.mqtt_client_connection.Client") as MockClient,
    ):
        mock_settings = MockSettings.return_value
        mock_settings.MQTT_BROKER_CLIENT_NAME = "test_client"
        mock_settings.MQTT_BROKER_HOST = "localhost"
        mock_settings.MQTT_BROKER_PORT = 1883
        mock_settings.MQTT_BROKER_KEEPALIVE = 60

        mock_client = MockClient.return_value
        mock_client.is_connected.return_value = True

        conn = MQTTClientConnection()
        conn.mqtt_client = mock_client
        yield conn, mock_client


def test_connect(mqtt_client_conn: Tuple[MQTTClientConnection, Mock]) -> None:
    conn, mock_client = mqtt_client_conn
    conn.connect()
    mock_client.connect.assert_called_once()
    assert conn._is_connected is True


def test_disconnect(mqtt_client_conn: Tuple[MQTTClientConnection, Mock]) -> None:
    conn, mock_client = mqtt_client_conn
    conn._is_connected = True  # força estado
    conn.disconnect()
    mock_client.disconnect.assert_called_once()
    assert conn._is_connected is False


def test_is_connected(mqtt_client_conn: Tuple[MQTTClientConnection, Mock]) -> None:
    conn, _ = mqtt_client_conn
    assert conn.is_connected() is True

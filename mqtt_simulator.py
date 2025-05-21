# simulador_mqtt.py

import json
import random
import time

import paho.mqtt.client as mqtt

# ! Configurações do broker MQTT LOCAL
broker = (
    "test.mosquitto.org"  # ? as vezes o mosquitto não está disponível usar localhost
)
port = 1883
topic = "/roger/teste"

# Criação do cliente MQTT
mqtt_client = mqtt.Client()

# Conexão com o broker local
mqtt_client.connect(broker, port)
mqtt_client.loop_start()

# Envio contínuo de dados simulados
print(f"Enviando dados simulados para o tópico '{topic}'...")

try:
    while True:
        payload = {
            "uid": "UID-456",
            "temp": random.randint(5, 30),
            "umidade": random.randint(80, 95),
            "unixtime": int(time.time()),
        }

        mqtt_client.publish(topic, json.dumps(payload))
        print(f"Dados enviados: {payload}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Simulação encerrada.")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

import json
import time

import paho.mqtt.client as mqtt

# Configurações do broker MQTT
broker = "test.mosquitto.org"
port = 1883
topic = "/newData"

# Cria o cliente MQTT
mqtt_client = mqtt.Client()

# Conecta ao broker MQTT
mqtt_client.connect(broker, port)

# Simula o envio de dados
print("Enviando dados simulados para o tópico MQTT...")
while True:
    payload = {
        "uid": "123",
        "temperature": 25.5,
        "humidity": 60,
        "timestamp": int(time.time()),
    }

    # Converte o payload para JSON e publica no tópico
    mqtt_client.publish(topic, json.dumps(payload))
    print(f"Dados enviados para o tópico '{topic}': {payload}")
    time.sleep(15)

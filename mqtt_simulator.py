# simulador_mqtt.py

import json
import time

import paho.mqtt.client as mqtt

# Configurações do broker MQTT LOCAL
broker = "localhost"  # Ou 127.0.0.1
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
            "uid": "UID-123",
            "temp": 30,
            "umidade": 40,
            "unixtime": int(time.time()),
        }

        mqtt_client.publish(topic, json.dumps(payload))
        print(f"Dados enviados: {payload}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Simulação encerrada.")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

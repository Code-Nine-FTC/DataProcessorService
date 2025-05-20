import paho.mqtt.client as mqtt

broker = (
    "test.mosquitto.org"  # ? as vezes o mosquitto não está disponível usar localhost
)
port = 1883
topic = "/roger/teste"


def on_connect(client, userdata, flags, rc) -> None:  # type: ignore[no-untyped-def]
    print("Conectado com código:", rc)
    client.subscribe(topic)


def on_message(client, userdata, msg) -> None:  # type: ignore[no-untyped-def]
    print(f"Mensagem recebida do tópico {msg.topic}: {msg.payload.decode()}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_forever()

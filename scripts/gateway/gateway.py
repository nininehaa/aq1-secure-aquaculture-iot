import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "aquaculture/sensors/#"

def on_message(client, userdata, message):
    value = message.payload.decode()

    print(
        f"Gateway received from {message.topic}: {value}"
    )

client = mqtt.Client()

client.on_message = on_message

client.connect(broker, port, 60)

client.subscribe(topic)

print("Gateway is listening for sensor readings...")

client.loop_forever()
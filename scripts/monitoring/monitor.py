from datetime import datetime
import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "aquaculture/sensors/#"

def on_message(client, userdata, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value = message.payload.decode()

    log_line = f"{timestamp} | {message.topic} | {value}"

    print(log_line)

    with open("sensor.log", "a") as file:
        file.write(log_line + "\n")

client = mqtt.Client()

client.on_message = on_message
client.connect(broker, port, 60)
client.subscribe(topic)

print("Monitoring started...")

client.loop_forever()
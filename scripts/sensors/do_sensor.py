import random
import time
import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "aquaculture/sensors/dissolved_oxygen"

client = mqtt.Client()
client.connect(broker, port, 60)

while True:
    value = round(random.uniform(5.0, 9.0), 2)

    client.publish(topic, str(value))

    print(f"Published dissolved oxygen: {value} mg/L")

    time.sleep(5)
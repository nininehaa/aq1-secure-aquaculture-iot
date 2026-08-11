import hashlib
import hmac
import json
import random
import time

import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883
TOPIC = "aquaculture/sensors/dissolved_oxygen"

SENSOR_ID = "sensor01"
SENSOR_TYPE = "DO"
SECRET_KEY = b"aq1-week5-secret-key"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    value = round(random.uniform(5.0, 9.0), 2)

    message = f"{SENSOR_ID}|{SENSOR_TYPE}|{value}"

    # Generate the HMAC-SHA256 signature.
    signature = hmac.new(
        SECRET_KEY,
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

  
    payload = {
        "sensor_id": SENSOR_ID,
        "sensor_type": SENSOR_TYPE,
        "value": value,
        "hmac": signature,
    }

    client.publish(TOPIC, json.dumps(payload))

    print(f"Published dissolved oxygen: {value} mg/L")
    print(f"HMAC: {signature}")

    time.sleep(5)
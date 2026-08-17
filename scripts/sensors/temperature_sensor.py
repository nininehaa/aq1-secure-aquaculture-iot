import json
import random
import time
import os
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883
TOPIC = "aq1/pond1/temperature"
MQTT_USERNAME = os.getenv("AQ1_MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("AQ1_MQTT_PASSWORD")

SENSOR_ID = "TEMP-001"
POND_ID = "POND-01"


def generate_temperature():
    """Simulate a realistic aquaculture water-temperature reading."""
    return round(random.uniform(24.0, 30.0), 2)


def create_message():
    temperature = generate_temperature()

    if temperature < 25:
        status = "LOW"
    elif temperature > 29:
        status = "HIGH"
    else:
        status = "NORMAL"

    return {
        "sensor_id": SENSOR_ID,
        "pond_id": POND_ID,
        "sensor_type": "temperature",
        "value": temperature,
        "unit": "C",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=SENSOR_ID
)

client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD
)

try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("AQ-1 Temperature Sensor Simulator")
    print("--------------------------------")
    print(f"Sensor ID : {SENSOR_ID}")
    print(f"Pond      : {POND_ID}")
    print(f"MQTT Topic: {TOPIC}")
    print()

    while True:
        message = create_message()

        client.publish(
            TOPIC,
            json.dumps(message)
        )

        print(
            f"[{message['timestamp']}] "
            f"{message['sensor_id']} -> "
            f"{message['value']} °C "
            f"({message['status']})"
        )

        time.sleep(5)

except KeyboardInterrupt:
    print("\nTemperature sensor stopped.")

finally:
    client.loop_stop()
    client.disconnect()
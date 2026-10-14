import hashlib
import hmac
import json
import os
import random
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "aquaculture/sensors/ph"

SENSOR_ID = "PH-001"
POND_ID = "POND-01"
SENSOR_TYPE = "ph"
UNIT = "pH"

SECRET_KEY = os.environ.get("AQ1_SENSOR_KEY", "").encode("utf-8")

if not SECRET_KEY:
    raise RuntimeError("AQ1_SENSOR_KEY environment variable is missing")

SEQUENCE_FILE = "/root/ph_sequence.txt"

def load_sequence():
    try:
        with open(SEQUENCE_FILE, "r") as f:
            sequence = int(f.read().strip())
        if sequence < 0:
            raise ValueError("Invalid sequence")
        return sequence
    except FileNotFoundError:
        return 0

def save_sequence(sequence):
    temp_file = SEQUENCE_FILE + ".tmp"

    with open(temp_file, "w") as f:
        f.write(str(sequence))
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_file, SEQUENCE_FILE)

sequence = load_sequence()

client = mqtt.Client()

print("Connecting to MQTT broker...")
client.connect(BROKER, PORT, 60)
client.loop_start()

print("Connected.")
print("==============================")
print(" AQ-1 pH Sensor V2")
print("==============================")
print(f"Sensor ID: {SENSOR_ID}")
print(f"Pond:      {POND_ID}")
print(f"Topic:     {TOPIC}")
print(f"Starting sequence: {sequence}")
print()

try:
    while True:
        sequence += 1
        save_sequence(sequence)

        value = round(random.uniform(7.0, 8.2), 1)
        timestamp = int(time.time())

        protected_message = (
            f"{SENSOR_ID}|{POND_ID}|{SENSOR_TYPE}|"
            f"{value:.1f}|{UNIT}|{timestamp}|{sequence}"
        )

        signature = hmac.new(
            SECRET_KEY,
            protected_message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        payload = {
            "sensor_id": SENSOR_ID,
            "pond_id": POND_ID,
            "sensor_type": SENSOR_TYPE,
            "value": value,
            "unit": UNIT,
            "timestamp": timestamp,
            "sequence": sequence,
            "hmac": signature
        }

        print("--------------------------------")
        print(f"pH Reading: {value}")
        print(f"Timestamp: {timestamp}")
        print(f"Sequence: {sequence}")
        print(f"Protected: {protected_message}")

        result = client.publish(
            TOPIC,
            json.dumps(payload)
        )

        result.wait_for_publish()

        print("MQTT publish: SUCCESS" if result.rc == 0 else "MQTT publish: FAILED")

        time.sleep(5)

except KeyboardInterrupt:
    print("\npH sensor stopped.")

finally:
    client.loop_stop()
    client.disconnect()

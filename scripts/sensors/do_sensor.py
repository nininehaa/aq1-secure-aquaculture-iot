import hashlib
import hmac
import json
import os
import random
import time
import paho.mqtt.client as mqtt

# ==========================================
# AQ-1 DO SENSOR — SECURITY V2
# ==========================================

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "aquaculture/sensors/dissolved_oxygen"

SENSOR_ID = "DO-001"
POND_ID = "POND-01"
SENSOR_TYPE = "dissolved_oxygen"
UNIT = "mg/L"

# Use the same key as the current gateway for now.
# We'll introduce individual sensor keys later.
SECRET_KEY = os.environ.get(
    "AQ1_SENSOR_KEY", ""
).encode("utf-8")

if not SECRET_KEY:
    raise RuntimeError("AQ1_SENSOR_KEY environment variable is missing")



# Persist the sequence number across sensor restarts
SEQUENCE_FILE = "/root/do_sequence.txt"

def load_sequence():
    try:
        with open(SEQUENCE_FILE, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def save_sequence(value):
    temp_file = SEQUENCE_FILE + ".tmp"

    with open(temp_file, "w") as f:
        f.write(str(value))
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_file, SEQUENCE_FILE)

sequence = load_sequence()



client = mqtt.Client()

print("Connecting to MQTT broker...")
client.connect(BROKER, PORT, 60)
client.loop_start()

print("===================================")
print(" AQ-1 DO SENSOR — SECURITY V2")
print("===================================")
print(f"Sensor: {SENSOR_ID}")
print(f"Pond:   {POND_ID}")
print("Security: HMAC + Timestamp + Sequence")
print()

try:
    while True:

        sequence += 1
        save_sequence(sequence)

        value = round(random.uniform(5.5, 7.5), 1)
        timestamp = int(time.time())

        protected_message = (
            f"{SENSOR_ID}|"
            f"{POND_ID}|"
            f"{SENSOR_TYPE}|"
            f"{value:.1f}|"
            f"{UNIT}|"
            f"{timestamp}|"
            f"{sequence}"
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

        print("-----------------------------------")
        print(f"Reading:  {value} {UNIT}")
        print(f"Time:     {timestamp}")
        print(f"Sequence: {sequence}")
        print(f"HMAC:     {signature[:16]}...")

        result = client.publish(
            TOPIC,
            json.dumps(payload)
        )

        result.wait_for_publish()

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("MQTT publish: SUCCESS")
        else:
            print(f"MQTT publish error: {result.rc}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nDO sensor stopped.")

finally:
    client.loop_stop()
    client.disconnect()

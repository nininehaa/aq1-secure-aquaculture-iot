import hashlib
import hmac
import json
import os
import threading
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from azure_sender import (
    configured as azure_configured,
    send_controller_state,
    send_physical_verified,
    send_security_event,
)

BROKER = os.getenv("AQ1_MQTT_HOST", "localhost")
PORT = int(os.getenv("AQ1_MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("AQ1_MQTT_USERNAME", "aq1_monitor")
MQTT_PASSWORD = os.getenv("AQ1_MQTT_PASSWORD")
TEMP_HMAC_KEY = os.getenv("AQ1_TEMP_HMAC_KEY")

TEMP_TOPIC = "aq1/pond1/temperature"
CONTROLLER_TOPIC = "aq1/controller/state"
SENSOR_ID = "TEMP-001"
SENSOR_TIMEOUT = int(os.getenv("AQ1_SENSOR_TIMEOUT", "10"))

if not TEMP_HMAC_KEY:
    raise RuntimeError("AQ1_TEMP_HMAC_KEY is not configured.")
if not MQTT_PASSWORD:
    raise RuntimeError("AQ1_MQTT_PASSWORD is not configured.")

last_valid = None
outage_reported = False
controller_state = None
state_lock = threading.Lock()


def stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def verify_temperature(payload):
    required = {
        "sensor_id",
        "pond_id",
        "sensor_type",
        "value",
        "unit",
        "status",
        "timestamp",
        "hmac",
    }
    if not required.issubset(payload):
        return False, "required fields missing"
    if payload["sensor_id"] != SENSOR_ID:
        return False, "unknown sensor identity"
    if payload["sensor_type"] != "temperature":
        return False, "invalid sensor type"
    if not isinstance(payload["hmac"], str):
        return False, "invalid HMAC field"

    signed = (
        f'{payload["sensor_id"]}|'
        f'{payload["pond_id"]}|'
        f'{payload["sensor_type"]}|'
        f'{payload["value"]}|'
        f'{payload["unit"]}|'
        f'{payload["status"]}|'
        f'{payload["timestamp"]}'
    )
    expected = hmac.new(
        TEMP_HMAC_KEY.encode("utf-8"),
        signed.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(payload["hmac"], expected):
        return False, "HMAC verification failed"
    return True, "HMAC valid"


def set_controller(client, state, reason):
    global controller_state
    if controller_state == state:
        return

    controller_state = state
    payload = {
        "state": state,
        "sensor_id": SENSOR_ID,
        "reason": reason,
        "timestamp": stamp(),
    }
    client.publish(CONTROLLER_TOPIC, json.dumps(payload), qos=0, retain=True)
    print(f"{stamp()} | CONTROLLER | STATE: {state} | Sensor: {SENSOR_ID} | Reason: {reason}")

    if azure_configured():
        send_controller_state(state, reason, payload["timestamp"])


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to MQTT broker at {BROKER}:{PORT}")
        print(f"Subscribed to: {TEMP_TOPIC}")
        print(f"Azure forwarding: {'ENABLED' if azure_configured() else 'DISABLED'}")
        client.subscribe(TEMP_TOPIC, 0)
    else:
        print(f"MQTT connection failed: {reason_code}")


def on_message(client, userdata, message):
    global last_valid, outage_reported

    try:
        payload = json.loads(message.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        reason = "Unreadable/non-JSON payload"
        print(f"{stamp()} | SECURITY ALERT | Temperature reading rejected | Reason: {reason}")
        set_controller(client, "SAFE/HOLD", reason)
        if azure_configured():
            send_security_event("TEMPERATURE REJECTED", SENSOR_ID, reason)
        return

    valid, reason = verify_temperature(payload)
    if not valid:
        print(
            f"{stamp()} | SECURITY ALERT | Temperature reading rejected | "
            f"Sensor: {SENSOR_ID} | Reason: {reason}"
        )
        set_controller(client, "SAFE/HOLD", reason)
        if azure_configured():
            send_security_event("HMAC/IDENTITY REJECTED", SENSOR_ID, reason)
        return

    with state_lock:
        was_offline = outage_reported
        last_valid = time.time()
        outage_reported = False

    if was_offline:
        print(f"{stamp()} | RECOVERY | Temperature sensor {SENSOR_ID} is online again")
        if azure_configured():
            send_security_event("RECOVERY", SENSOR_ID, "Valid HMAC telemetry restored")

    set_controller(client, "NORMAL", "Valid HMAC telemetry available")

    print(
        f"{stamp()} | ACCEPTED | Sensor: {SENSOR_ID} | "
        f"Value: {payload.get('value')} {payload.get('unit', 'C')} | HMAC: VALID"
    )

    if azure_configured():
        send_physical_verified(payload)


def outage_watch(client):
    global outage_reported

    while True:
        time.sleep(1)
        with state_lock:
            seen = last_valid
            already = outage_reported

        if seen is None or already:
            continue

        age = time.time() - seen
        if age > SENSOR_TIMEOUT:
            with state_lock:
                if outage_reported:
                    continue
                outage_reported = True

            reason = f"No valid reading for more than {SENSOR_TIMEOUT} seconds"
            print(
                f"{stamp()} | OUTAGE ALERT | Temperature sensor {SENSOR_ID} unavailable | {reason}"
            )
            set_controller(client, "SAFE/HOLD", reason)
            if azure_configured():
                send_security_event("OUTAGE ALERT", SENSOR_ID, reason)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="AQ1-PHYSICAL-MONITOR",
)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

threading.Thread(target=outage_watch, args=(client,), daemon=True).start()

print("AQ-1 Physical ESP32 Security Monitor + Azure")
print("------------------------------------------")
print(f"Sensor: {SENSOR_ID}")
print(f"Outage timeout: {SENSOR_TIMEOUT} seconds")
print("HMAC-SHA256 verification: ENABLED")

try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
finally:
    client.disconnect()

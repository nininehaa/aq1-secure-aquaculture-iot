import hashlib
import hmac
import json
import os
import random
import threading
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


# ==================================================
# AQ-1 SECURE TEMPERATURE SENSOR
# Coral Coast Aquaculture
# ==================================================

BROKER = "localhost"
PORT = 1883
TOPIC = "aq1/pond1/temperature"

SENSOR_ID = "TEMP-001"
POND_ID = "POND-01"
SENSOR_TYPE = "temperature"
UNIT = "C"

PUBLISH_INTERVAL = 5


# ==================================================
# SECURITY CONFIGURATION
# Secrets are loaded from environment variables.
# They are NOT stored in the GitHub repository.
# ==================================================

MQTT_USERNAME = os.getenv("AQ1_MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("AQ1_MQTT_PASSWORD")
TEMP_HMAC_KEY = os.getenv("AQ1_TEMP_HMAC_KEY")


if not MQTT_USERNAME:
    raise RuntimeError(
        "AQ1_MQTT_USERNAME is not configured."
    )

if not MQTT_PASSWORD:
    raise RuntimeError(
        "AQ1_MQTT_PASSWORD is not configured."
    )

if not TEMP_HMAC_KEY:
    raise RuntimeError(
        "AQ1_TEMP_HMAC_KEY is not configured."
    )


# ==================================================
# CONNECTION STATE
# ==================================================

connected_event = threading.Event()


# ==================================================
# SENSOR FUNCTIONS
# ==================================================

def generate_temperature():
    """
    Simulate realistic aquaculture
    water temperature between 24 and 30 C.
    """

    return round(
        random.uniform(24.0, 30.0),
        2,
    )


def determine_status(value):
    """
    Convert the temperature reading
    into a simple operational status.
    """

    if value < 25.0:
        return "LOW"

    if value > 29.0:
        return "HIGH"

    return "NORMAL"


def create_signed_string(
    sensor_id,
    pond_id,
    sensor_type,
    value,
    unit,
    status,
    timestamp,
):
    """
    Canonical message format.

    Neha's verification component MUST use
    this exact field order and separator.
    """

    return (
        f"{sensor_id}|"
        f"{pond_id}|"
        f"{sensor_type}|"
        f"{value}|"
        f"{unit}|"
        f"{status}|"
        f"{timestamp}"
    )


def generate_hmac(signed_message):
    """
    Generate HMAC-SHA256 message signature.
    """

    return hmac.new(
        TEMP_HMAC_KEY.encode("utf-8"),
        signed_message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def create_message():
    """
    Generate one complete authenticated
    temperature sensor payload.
    """

    value = generate_temperature()
    status = determine_status(value)

    timestamp = (
        datetime.now(timezone.utc)
        .isoformat()
    )

    signed_message = create_signed_string(
        SENSOR_ID,
        POND_ID,
        SENSOR_TYPE,
        value,
        UNIT,
        status,
        timestamp,
    )

    signature = generate_hmac(
        signed_message
    )

    return {
        "sensor_id": SENSOR_ID,
        "pond_id": POND_ID,
        "sensor_type": SENSOR_TYPE,
        "value": value,
        "unit": UNIT,
        "status": status,
        "timestamp": timestamp,
        "hmac": signature,
    }


# ==================================================
# MQTT CALLBACKS
# ==================================================

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties,
):
    if reason_code == 0:

        print(
            "MQTT authentication successful."
        )

        print(
            "Connected to secure "
            "Mosquitto broker."
        )

        connected_event.set()

    else:

        print(
            "MQTT connection rejected. "
            f"Reason: {reason_code}"
        )


def on_disconnect(
    client,
    userdata,
    disconnect_flags,
    reason_code,
    properties,
):
    connected_event.clear()


# ==================================================
# MQTT CLIENT
# ==================================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=SENSOR_ID,
)

client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD,
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect


# ==================================================
# MAIN SENSOR LOOP
# ==================================================

try:

    print()
    print(
        "AQ-1 Secure Temperature Sensor"
    )
    print(
        "================================"
    )
    print(f"Sensor ID   : {SENSOR_ID}")
    print(f"Pond        : {POND_ID}")
    print(f"Topic       : {TOPIC}")
    print("MQTT Auth   : ENABLED")
    print("HMAC-SHA256 : ENABLED")
    print()

    client.connect(
        BROKER,
        PORT,
        60,
    )

    client.loop_start()

    if not connected_event.wait(timeout=5):

        raise RuntimeError(
            "Could not establish an "
            "authenticated MQTT connection."
        )

    while True:

        message = create_message()

        payload = json.dumps(
            message,
            separators=(",", ":"),
        )

        publish_result = client.publish(
            TOPIC,
            payload,
            qos=1,
        )

        publish_result.wait_for_publish()

        print(
            f"{message['timestamp']} | "
            f"{SENSOR_ID} | "
            f"{message['value']} {UNIT} | "
            f"{message['status']}"
        )

        print(
            "HMAC-SHA256: "
            f"{message['hmac']}"
        )

        print(
            "SECURE READING PUBLISHED"
        )

        print()

        time.sleep(
            PUBLISH_INTERVAL
        )


except KeyboardInterrupt:

    print()
    print(
        "Temperature sensor stopped."
    )


except Exception as error:

    print()
    print(
        "TEMPERATURE SENSOR ERROR:"
    )

    print(error)


finally:

    client.loop_stop()

    try:
        client.disconnect()

    except Exception:
        pass
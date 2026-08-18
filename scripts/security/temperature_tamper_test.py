import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


# ==================================================
# AQ-1 TEMPERATURE TAMPER TEST
#
# Creates a legitimate signed message,
# changes the temperature AFTER signing,
# then publishes the modified payload.
#
# A correctly configured monitor should reject it.
# ==================================================

BROKER = "localhost"
PORT = 1883
TOPIC = "aq1/pond1/temperature"

SENSOR_ID = "TEMP-001"
POND_ID = "POND-01"
SENSOR_TYPE = "temperature"
UNIT = "C"


# ==================================================
# SECURITY CONFIGURATION
# ==================================================

MQTT_USERNAME = os.getenv(
    "AQ1_MQTT_USERNAME"
)

MQTT_PASSWORD = os.getenv(
    "AQ1_MQTT_PASSWORD"
)

TEMP_HMAC_KEY = os.getenv(
    "AQ1_TEMP_HMAC_KEY"
)


if not MQTT_USERNAME:
    raise RuntimeError(
        "AQ1_MQTT_USERNAME is missing."
    )

if not MQTT_PASSWORD:
    raise RuntimeError(
        "AQ1_MQTT_PASSWORD is missing."
    )

if not TEMP_HMAC_KEY:
    raise RuntimeError(
        "AQ1_TEMP_HMAC_KEY is missing."
    )


# ==================================================
# CREATE VALID SIGNATURE
# ==================================================

def create_signature(
    value,
    status,
    timestamp,
):

    signed_message = (
        f"{SENSOR_ID}|"
        f"{POND_ID}|"
        f"{SENSOR_TYPE}|"
        f"{value}|"
        f"{UNIT}|"
        f"{status}|"
        f"{timestamp}"
    )

    return hmac.new(
        TEMP_HMAC_KEY.encode("utf-8"),
        signed_message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


# ==================================================
# ORIGINAL LEGITIMATE SENSOR DATA
# ==================================================

original_value = 27.20
original_status = "NORMAL"

timestamp = (
    datetime.now(timezone.utc)
    .isoformat()
)

signature = create_signature(
    original_value,
    original_status,
    timestamp,
)


# ==================================================
# SIMULATED TAMPERING
#
# The attacker changes the reading AFTER
# the HMAC has already been generated.
#
# Therefore the HMAC no longer matches
# the contents of the message.
# ==================================================

tampered_value = 41.20
tampered_status = "HIGH"


payload = {
    "sensor_id": SENSOR_ID,
    "pond_id": POND_ID,
    "sensor_type": SENSOR_TYPE,

    # Tampered after signing
    "value": tampered_value,

    "unit": UNIT,

    # Tampered after signing
    "status": tampered_status,

    "timestamp": timestamp,

    # This HMAC belongs to the ORIGINAL data
    "hmac": signature,
}


# ==================================================
# MQTT CLIENT
# ==================================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="TEMP-TAMPER-TEST",
)

client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD,
)


# ==================================================
# PUBLISH TAMPERED MESSAGE
# ==================================================

try:

    client.connect(
        BROKER,
        PORT,
        60,
    )

    client.loop_start()

    result = client.publish(
        TOPIC,
        json.dumps(payload),
        qos=1,
    )

    result.wait_for_publish()

    print()
    print(
        "AQ-1 Temperature Tamper Test"
    )

    print(
        "============================="
    )

    print(
        f"Original signed value : "
        f"{original_value} C"
    )

    print(
        f"Tampered value        : "
        f"{tampered_value} C"
    )

    print(
        f"Original status       : "
        f"{original_status}"
    )

    print(
        f"Tampered status       : "
        f"{tampered_status}"
    )

    print()

    print(
        "Tampered MQTT payload published."
    )

    print()

    print(
        "Expected security result:"
    )

    print(
        "Monitor rejects message because "
        "HMAC verification fails."
    )

    print()


except Exception as error:

    print()
    print(
        "TAMPER TEST ERROR:"
    )

    print(error)


finally:

    client.loop_stop()

    try:
        client.disconnect()

    except Exception:
        pass
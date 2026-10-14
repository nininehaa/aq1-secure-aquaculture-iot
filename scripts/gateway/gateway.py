import os
import hashlib
import hmac
import json
import time
import threading

import paho.mqtt.client as mqtt


# ==========================================
# AQ-1 MQTT CONFIGURATION
# ==========================================

BROKER = "broker.hivemq.com"
PORT = 8000

# Existing GNS3 sensors
SENSOR_TOPIC = "aquaculture/sensors/#"

# NEW physical temperature sensor
PHYSICAL_TEMP_TOPIC = "aq1/pond1/temperature"

VERIFIED_TOPIC = "aquaculture/gateway/verified"
SECURITY_TOPIC = "aquaculture/events/security"
STATUS_TOPIC = "aquaculture/events/status"

# Existing DO / pH key
SECRET_KEY = b"aq1-week5-secret-key"

with open("/root/do_hmac.key", "r") as f:
    DO_HMAC_KEY = f.read().strip().encode("utf-8")

with open("/root/ph_hmac.key", "r") as f:
    PH_HMAC_KEY = f.read().strip().encode("utf-8")

# Physical TEMP-001 key
# Paste the TEMP_HMAC_KEY from secrets.h between the quotes.
TEMP_HMAC_KEY = b"6e72a6bdf2b35d0a7e4dec205cc3c7a3992f8bbeb095359e1893c28a5a8ca685"

OUTAGE_TIMEOUT = 10


# ==========================================
# SENSOR STATE
# ==========================================

last_seen = {}
offline_sensors = set()
# DO-001 replay protection
REPLAY_STATE_FILE = "/root/replay_state.json"


def load_replay_state():
    try:
        with open(REPLAY_STATE_FILE, "r") as f:
            state = json.load(f)

        for sensor_id in ("DO-001", "PH-001", "TEMP-001" ):
            value = state.get(sensor_id, 0)
            if type(value) is not int or value < 0:
                raise ValueError(f"Invalid sequence for {sensor_id}")
            state[sensor_id] = value

        return state

    except FileNotFoundError:
        raise RuntimeError(
            "Replay state file missing. Refusing to reset replay protection."
        )


def save_replay_state(sensor_id, sequence):
    if sensor_id not in ("DO-001", "PH-001", "TEMP-001"):
        raise ValueError("Unknown sensor ID")

    updated_state = replay_state.copy()
    updated_state[sensor_id] = sequence

    temp_file = REPLAY_STATE_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(updated_state, f)
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_file, REPLAY_STATE_FILE)

    replay_state.update(updated_state)


replay_state = load_replay_state()
last_do_sequence = replay_state["DO-001"]
last_ph_sequence = replay_state["PH-001"]
last_temp_sequence = replay_state["TEMP-001"]

print(f"Loaded TEMP-001 replay sequence: {last_temp_sequence}")
print(f"Loaded DO-001 replay sequence: {last_do_sequence}")
MAX_MESSAGE_AGE = 30
MAX_FUTURE_SKEW = 5

# ==========================================
# MQTT EVENT PUBLISHERS
# ==========================================

def publish_verified(
    sensor_id,
    sensor_type,
    value,
    unit,
    pond_id,
    sensor_status=None,
    sensor_timestamp=None
):

    event = {
        "event": "verified_reading",
        "sensor_id": sensor_id,
        "pond_id": pond_id,
        "sensor_type": sensor_type,
        "value": value,
        "unit": unit,
        "integrity": "VERIFIED",
        "status": "ONLINE",
        "timestamp": int(time.time())
    }

    # Preserve information from physical sensor
    if sensor_status is not None:
        event["sensor_status"] = sensor_status

    if sensor_timestamp is not None:
        event["sensor_timestamp"] = sensor_timestamp

    client.publish(
        VERIFIED_TOPIC,
        json.dumps(event)
    )


# ==========================================
# ATTACK CORRELATION
# ==========================================

from collections import defaultdict, deque

CORRELATION_WINDOW = 30
TAMPERING_THRESHOLD = 5

attack_history = defaultdict(deque)
last_correlation_alert = {}

def track_attack(sensor_id, attack_type):
    if attack_type != "MESSAGE_TAMPERING":
        return

    now = time.monotonic()
    key = (str(sensor_id), attack_type)
    history = attack_history[key]

    while history and now - history[0] > CORRELATION_WINDOW:
        history.popleft()

    history.append(now)

    if len(history) < TAMPERING_THRESHOLD:
        return

    if now - last_correlation_alert.get(key, -float("inf")) < CORRELATION_WINDOW:
        return

    last_correlation_alert[key] = now

    print(
        f"SECURITY CORRELATION: REPEATED_TAMPERING "
        f"detected for {sensor_id} "
        f"({len(history)} failures in 30s)"
    )

    publish_security_alert(
        sensor_id,
        "unknown",
        None,
        attack_type="REPEATED_TAMPERING",
        severity="HIGH",
        reason=(
            f"{len(history)} HMAC failures detected "
            f"within 30 seconds"
        )
    )


# ==========================================
# MULTI-VECTOR ATTACK CORRELATION
# ==========================================

MULTI_VECTOR_WINDOW = 60
MULTI_VECTOR_COOLDOWN = 60

multi_vector_history = defaultdict(deque)
last_multi_vector_alert = {}

def track_multi_vector(sensor_id, attack_type):
    # Correlation alerts must not correlate themselves.
    if attack_type in (
        "MULTI_VECTOR_ATTACK",
        "REPEATED_TAMPERING"
    ):
        return

    # UNKNOWN cannot reliably identify a target sensor.
    if sensor_id not in ("DO-001", "PH-001", "TEMP-001"):
        return

    now = time.monotonic()
    history = multi_vector_history[sensor_id]

    while history and now - history[0][0] > MULTI_VECTOR_WINDOW:
        history.popleft()

    history.append((now, attack_type))

    attack_types = {item[1] for item in history}

    if len(attack_types) < 2:
        return

    if now - last_multi_vector_alert.get(
        sensor_id, -float("inf")
    ) < MULTI_VECTOR_COOLDOWN:
        return

    last_multi_vector_alert[sensor_id] = now

    print(
        f"SECURITY CORRELATION: MULTI_VECTOR_ATTACK "
        f"detected for {sensor_id}: "
        f"{', '.join(sorted(attack_types))}"
    )

    publish_security_alert(
        sensor_id,
        "unknown",
        None,
        attack_type="MULTI_VECTOR_ATTACK",
        severity="CRITICAL",
        reason=(
            "Multiple attack types detected within "
            "60 seconds: "
            + ", ".join(sorted(attack_types))
        )
    )


SECURITY_ALERT_COOLDOWN = 10
last_security_alert = {}

def publish_security_alert(
    sensor_id,
    sensor_type,
    value,
    attack_type="MESSAGE_TAMPERING",
    severity="HIGH",
    reason="HMAC-SHA256 verification failed"
):
    # Track detected attack types before alert deduplication.
    track_multi_vector(sensor_id, attack_type)

    now = time.monotonic()
    alert_key = (str(sensor_id), str(attack_type))

    last_sent = last_security_alert.get(
        alert_key, -float("inf")
    )

    if now - last_sent < SECURITY_ALERT_COOLDOWN:
        print(
            f"SECURITY: Duplicate alert suppressed "
            f"({attack_type}, {sensor_id})"
        )
        return

    last_security_alert[alert_key] = now

    event = {
        "event": "spoofing_attempt",
        "attack_type": attack_type,
        "sensor_id": sensor_id,
        "sensor_type": sensor_type,
        "value": value,
        "integrity": "REJECTED",
        "severity": severity,
        "message": reason,
        "timestamp": int(time.time())
    }

    client.publish(
        SECURITY_TOPIC,
        json.dumps(event)
    )


def publish_status(
    sensor_id,
    status,
    message
):

    event = {
        "event": "sensor_status",
        "sensor_id": sensor_id,
        "status": status,
        "message": message,
        "timestamp": int(time.time())
    }

    client.publish(
        STATUS_TOPIC,
        json.dumps(event)
    )


# ==========================================
# MESSAGE FLOOD DETECTION
# ==========================================

from collections import defaultdict, deque

FLOOD_WINDOW = 10
FLOOD_THRESHOLD = 20
FLOOD_ALERT_COOLDOWN = 30

message_times = defaultdict(deque)
last_flood_alert = {}

def detect_message_flood(topic):
    now = time.monotonic()
    history = message_times[topic]

    while history and now - history[0] > FLOOD_WINDOW:
        history.popleft()

    history.append(now)

    if len(history) <= FLOOD_THRESHOLD:
        return False

    if now - last_flood_alert.get(topic, -float("inf")) >= FLOOD_ALERT_COOLDOWN:
        last_flood_alert[topic] = now

        print(
            f"SECURITY: MESSAGE_FLOODING detected "
            f"on {topic} ({len(history)} messages in 10s)"
        )

        publish_security_alert(
            "UNKNOWN",
            "unknown",
            None,
            attack_type="MESSAGE_FLOODING",
            severity="HIGH",
            reason=f"Excessive MQTT traffic on topic {topic}"
        )

    return True


# ==========================================
# SENSOR MESSAGE PROCESSING
# ==========================================

def on_message(client, userdata, message):

    # Detect excessive MQTT traffic before parsing the payload.
    # Detection only: legitimate messages continue processing.
    detect_message_flood(message.topic)

    try:

        payload = json.loads(
            message.payload.decode("utf-8")
        )

        sensor_id = payload["sensor_id"]
        pond_id = payload.get(
            "pond_id",
            "POND-01"
        )
        sensor_type = payload["sensor_type"]
        value = payload["value"]
        unit = payload.get("unit", "")
        received_hmac = payload["hmac"]

        sensor_status = None
        sensor_timestamp = None


        # ==================================
        # PHYSICAL TEMP-001
        # ==================================

        if message.topic == PHYSICAL_TEMP_TOPIC:
            if sensor_id != "TEMP-001" or pond_id != "POND-01" or sensor_type != "temperature":
                print(
                    f"REJECTED: Invalid physical sensor identity "
                    f"(sensor={sensor_id}, pond={pond_id}, type={sensor_type})"
                )
                publish_security_alert(
                    sensor_id,
                    sensor_type,
                    value,
                    attack_type="SENSOR_SPOOFING",
                    severity="HIGH",
                    reason="Invalid TEMP-001 sensor identity or pond ID"
                )
                return

            sensor_status = payload["status"]
            sensor_timestamp = payload["timestamp"]
            sequence = payload["sequence"]

            if type(sequence) is not int or sequence < 1:
                raise ValueError("Invalid TEMP-001 sequence")

            # IMPORTANT:
            # ESP32 signs value with 2 decimal places.
            value_string = f"{float(value):.2f}"

            protected_message = (
                f"{sensor_id}|"
                f"{pond_id}|"
                f"{sensor_type}|"
                f"{value_string}|"
                f"{unit}|"
                f"{sensor_status}|"
                f"{sensor_timestamp}|"
                f"{sequence}"
            )

            expected_hmac = hmac.new(
                TEMP_HMAC_KEY,
                protected_message.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()

            source = "PHYSICAL TEMP SENSOR"

        # ==================================
        # DO-001 — SECURITY V2
        # ==================================

        elif (
            (message.topic == "aquaculture/sensors/dissolved_oxygen" and sensor_id == "DO-001")
            or
            (message.topic == "aquaculture/sensors/ph" and sensor_id == "PH-001")
        ):

            sensor_timestamp = payload["timestamp"]
            sequence = payload["sequence"]

            # Validate required field types
            if (
                type(sensor_timestamp) is not int
                or type(sequence) is not int
                or sequence < 1
                or type(value) not in (int, float)
                or not isinstance(received_hmac, str)
            ):
                raise ValueError("Invalid DO-001 v2 fields")

            value_string = f"{float(value):.1f}"

            protected_message = (
                f"{sensor_id}|"
                f"{pond_id}|"
                f"{sensor_type}|"
                f"{value_string}|"
                f"{unit}|"
                f"{sensor_timestamp}|"
                f"{sequence}"
            )

            expected_hmac = hmac.new(
                DO_HMAC_KEY if sensor_id == "DO-001" else PH_HMAC_KEY,
                protected_message.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()

            source = (
                "GNS3 DO SENSOR V2"
                if sensor_id == "DO-001"
                else "GNS3 PH SENSOR V2"
            )
        else:
            print(
                f"REJECTED: Unrecognised sensor or MQTT topic "
                f"(sensor={sensor_id}, topic={message.topic})"
            )

            publish_security_alert(
                sensor_id,
                sensor_type,
                value,
                attack_type="UNAUTHORISED_TOPIC",
                severity="HIGH",
                reason=(
                    f"Sensor identity/topic mismatch: "
                    f"sensor={sensor_id}, topic={message.topic}"
                )
            )
            return

        # ==================================
        # DISPLAY RECEIVED MESSAGE
        # ==================================

        print()
        print("----------------------------------------")
        print(f"MQTT message received: {message.topic}")
        print(f"Source:            {source}")
        print(f"Sensor ID:         {sensor_id}")
        print(f"Sensor Type:       {sensor_type}")
        print(f"Value:             {value} {unit}")

        if sensor_status is not None:
            print(
                f"Sensor Status:     "
                f"{sensor_status}"
            )

        if sensor_timestamp is not None:
            print(
                f"Sensor Timestamp:  "
                f"{sensor_timestamp}|"
            )

        print(
            f"Protected Message: "
            f"{protected_message}"
        )


        # ==================================
        # VALID MESSAGE
        # ==================================

        if hmac.compare_digest(
            received_hmac,
            expected_hmac
        ):


            # ==================================
            # DO-001 REPLAY PROTECTION
            # ==================================

            if source in ("GNS3 DO SENSOR V2", "GNS3 PH SENSOR V2", "PHYSICAL TEMP SENSOR"):



                current_time = int(time.time())

                if source == "PHYSICAL TEMP SENSOR":
    # ESP32 currently sends millis(), not Unix time.
    # Sequence-based replay protection applies,
    # but timestamp freshness checking is deferred.
                    message_age = 0
                else:
                    message_age = current_time - sensor_timestamp
                if (
                    message_age > MAX_MESSAGE_AGE
                    or message_age < -MAX_FUTURE_SKEW
                ):
                    print(
                        f"REJECTED: stale/future {sensor_id} message "
                        f"(age={message_age}s)"
                    )

                    continue_processing = False

                elif sequence <= replay_state[sensor_id]:
                    print(f"REJECTED: replay detected (sequence={sequence}, last={replay_state[sensor_id]})")

                    continue_processing = False

                else:
                    try:
                        save_replay_state(sensor_id, sequence)
                    except OSError as e:
                        print(f"REJECTED: Cannot persist replay state: {e}")
                        return
                    continue_processing = True

                if not continue_processing:

                    attack_type = (
                        "STALE_MESSAGE"
                        if message_age > MAX_MESSAGE_AGE
                        or message_age < -MAX_FUTURE_SKEW
                        else "REPLAY_ATTACK"
                    )

                    publish_security_alert(
                        sensor_id,
                        sensor_type,
                        value,
                        attack_type=attack_type,
                        severity="HIGH",
                        reason=(
                            f"{attack_type} detected: "
                            f"sequence={sequence}, "
                            f"age={message_age}s"
                        )
                    )

                    print(
                        "SECURITY ALERT: "
                        f"Rejected {sensor_id} message"
                    )

                    return


            last_seen[sensor_id] = time.time()

            print()
            print(
                f"ACCEPTED: {sensor_id} reported "
                f"{sensor_type} = {value} {unit}"
            )

            print(
                "PASS: HMAC-SHA256 message "
                "integrity verified"
            )

            if (
                message.topic
                == PHYSICAL_TEMP_TOPIC
            ):
                print(
                    "SOURCE VERIFIED: "
                    "Remote physical temperature "
                    "sensor"
                )

            # Send trusted reading to dashboard
            publish_verified(
                sensor_id,
                sensor_type,
                value,
                unit,
                pond_id,
                sensor_status,
                sensor_timestamp
            )


            # Sensor recovered
            if sensor_id in offline_sensors:

                offline_sensors.remove(
                    sensor_id
                )

                print()
                print(
                    f"RECOVERY: {sensor_id} "
                    "is ONLINE again"
                )

                publish_status(
                    sensor_id,
                    "ONLINE",
                    "Authenticated sensor "
                    "readings restored"
                )


        # ==================================
        # INVALID / SPOOFED MESSAGE
        # ==================================

        else:

            print()
            print(
                f"REJECTED: integrity check "
                f"failed for {sensor_id}"
            )

            print(
                "FAIL: HMAC-SHA256 "
                "verification failed"
            )

            print(
                "SECURITY: Invalid message "
                "ignored for outage monitoring"
            )

            track_attack(
                sensor_id,
                "MESSAGE_TAMPERING"
            )

            publish_security_alert(
                sensor_id,
                sensor_type,
                value
            )


    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError
    ) as error:

        print(
            f"REJECTED: invalid sensor "
            f"payload ({error})"
        )


# ==========================================
# OUTAGE MONITOR
# ==========================================

def monitor_outages():

    while True:

        current_time = time.time()

        for sensor_id, timestamp in list(
            last_seen.items()
        ):

            elapsed = (
                current_time - timestamp
            )

            if (
                elapsed > OUTAGE_TIMEOUT
                and sensor_id
                not in offline_sensors
            ):

                offline_sensors.add(
                    sensor_id
                )

                print()
                print(
                    "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                )
                print(
                    " SENSOR OUTAGE DETECTED"
                )
                print(
                    "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                )
                print(
                    f"Sensor: {sensor_id}"
                )
                print(
                    f"No authenticated reading "
                    f"for {elapsed:.1f} seconds"
                )
                print(
                    "Status: OFFLINE"
                )
                print()
                print(
                    "SAFE STATE: Do not rely "
                    "on stale sensor data."
                )
                print(
                    "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                )

                publish_status(
                    sensor_id,
                    "OFFLINE",
                    "No authenticated reading for "
                    f"{elapsed:.1f} seconds - "
                    "SAFE STATE ACTIVE"
                )

        time.sleep(1)


# ==========================================
# START GATEWAY
# ==========================================

client = mqtt.Client(client_id="aq1-gateway-main", transport="websockets")
client.ws_set_options(path="/mqtt")
client.on_message = on_message

def on_connect(client, userdata, flags, rc):
    print("MQTT CONNECT RESULT:", rc, flush=True)
    if rc == 0:
        client.subscribe("aquaculture/sensors/#")
        client.subscribe("aq1/pond1/temperature")
        print("MQTT SUBSCRIPTIONS REQUESTED", flush=True)

client.on_connect = on_connect

print(
    "========================================"
)
print(
    " AQ-1 Secure Pond Gateway"
)
print(
    "========================================"
)
print(
    f"Broker:              {BROKER}"
)
print(
    f"GNS3 sensor topic:   {SENSOR_TOPIC}"
)
print(
    f"Physical TEMP topic: "
    f"{PHYSICAL_TEMP_TOPIC}"
)
print(
    f"Verified topic:      {VERIFIED_TOPIC}"
)
print(
    f"Security topic:      {SECURITY_TOPIC}"
)
print(
    f"Status topic:        {STATUS_TOPIC}"
)
print(
    f"Outage timeout:      "
    f"{OUTAGE_TIMEOUT} seconds"
)
print()

client.connect(
    BROKER,
    PORT,
    60
)

# Existing DO / pH
client.subscribe(
    SENSOR_TOPIC
)

# NEW physical temperature sensor
client.subscribe(
    PHYSICAL_TEMP_TOPIC
)

monitor_thread = threading.Thread(
    target=monitor_outages,
    daemon=True
)

monitor_thread.start()

print("Connected.")
print(
    "Gateway is monitoring GNS3 and "
    "remote physical sensor readings..."
)

client.loop_forever()

import json
import threading
import time
from datetime import datetime

import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883

TOPICS = [
    ("aquaculture/sensors/#", 0),
    ("aq1/pond1/#", 0),
]

SENSOR_TIMEOUT = 10

EXPECTED_SENSORS = {
    "sensor01": "Dissolved oxygen",
    "TEMP-001": "Temperature",
}

last_valid_message = {
    sensor_id: None
    for sensor_id in EXPECTED_SENSORS
}

outage_reported = {
    sensor_id: False
    for sensor_id in EXPECTED_SENSORS
}

state_lock = threading.Lock()


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_log(line):
    with open("sensor.log", "a", encoding="utf-8") as file:
        file.write(line + "\n")


def log_event(line):
    print(line)
    write_log(line)


def detect_sensor_id(payload, topic):
    if isinstance(payload, dict):
        sensor_id = payload.get("sensor_id")

        if sensor_id in EXPECTED_SENSORS:
            return sensor_id

    if "dissolved_oxygen" in topic:
        return "sensor01"

    if "temperature" in topic:
        return "TEMP-001"

    return None


def record_valid_reading(sensor_id):
    with state_lock:
        was_offline = outage_reported[sensor_id]

        last_valid_message[sensor_id] = time.time()
        outage_reported[sensor_id] = False

    if was_offline:
        log_event(
            f"{current_timestamp()} | RECOVERY | "
            f"{EXPECTED_SENSORS[sensor_id]} sensor {sensor_id} "
            f"is online again"
        )


def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties,
):
    if reason_code == 0:
        print(
            f"Connected to MQTT broker at "
            f"{BROKER}:{PORT}"
        )

        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"Subscribed to: {topic}")

    else:
        print(
            f"MQTT connection failed: "
            f"{reason_code}"
        )


def on_message(client, userdata, message):
    timestamp = current_timestamp()

    try:
        decoded_payload = (
            message.payload.decode("utf-8")
        )

    except UnicodeDecodeError:
        log_event(
            f"{timestamp} | SECURITY ALERT | "
            f"Unreadable payload rejected | "
            f"Topic: {message.topic}"
        )
        return

    try:
        payload = json.loads(decoded_payload)

    except json.JSONDecodeError:
        payload = decoded_payload

    sensor_id = detect_sensor_id(
        payload,
        message.topic,
    )

    if sensor_id is None:
        log_event(
            f"{timestamp} | SECURITY ALERT | "
            f"Unknown sensor message | "
            f"Topic: {message.topic}"
        )
        return

    record_valid_reading(sensor_id)

    if isinstance(payload, dict):
        sensor_type = payload.get(
            "sensor_type",
            "UNKNOWN",
        )

        value = payload.get(
            "value",
            "UNKNOWN",
        )

        unit = payload.get(
            "unit",
            "",
        )

        if sensor_type == "DO" and not unit:
            unit = "mg/L"

        log_line = (
            f"{timestamp} | RECEIVED | "
            f"Sensor: {sensor_id} | "
            f"Type: {sensor_type} | "
            f"Value: {value} {unit}"
        )

    else:
        log_line = (
            f"{timestamp} | RECEIVED | "
            f"Sensor: {sensor_id} | "
            f"Topic: {message.topic} | "
            f"Value: {payload}"
        )

    log_event(log_line)


def check_sensor_outages():
    while True:
        current_time = time.time()
        alerts = []

        with state_lock:
            for (
                sensor_id,
                sensor_name,
            ) in EXPECTED_SENSORS.items():

                last_seen = (
                    last_valid_message[sensor_id]
                )

                if last_seen is None:
                    continue

                seconds_without_data = (
                    current_time - last_seen
                )

                if (
                    seconds_without_data
                    > SENSOR_TIMEOUT
                    and not outage_reported[
                        sensor_id
                    ]
                ):
                    outage_reported[
                        sensor_id
                    ] = True

                    alerts.append(
                        f"{current_timestamp()} | "
                        f"OUTAGE ALERT | "
                        f"{sensor_name} sensor "
                        f"{sensor_id} unavailable | "
                        f"No reading for more than "
                        f"{SENSOR_TIMEOUT} seconds"
                    )

        for alert in alerts:
            log_event(alert)

        time.sleep(1)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="AQ1-MONITOR",
)

client.on_connect = on_connect
client.on_message = on_message

outage_thread = threading.Thread(
    target=check_sensor_outages,
    daemon=True,
)

try:
    client.connect(
        BROKER,
        PORT,
        60,
    )

    print("AQ-1 Multi-Sensor Monitor")
    print("-------------------------")
    print(
        f"Outage timeout: "
        f"{SENSOR_TIMEOUT} seconds"
    )

    print("Expected sensors:")

    for (
        sensor_id,
        sensor_name,
    ) in EXPECTED_SENSORS.items():
        print(
            f"- {sensor_name}: "
            f"{sensor_id}"
        )

    print()

    outage_thread.start()
    client.loop_forever()

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    client.disconnect()
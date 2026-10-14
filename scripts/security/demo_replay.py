import json
import time
import threading
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "aquaculture/sensors/dissolved_oxygen"

captured = threading.Event()
original_payload = None
captured_sequence = None

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("[CONNECTED] Waiting for legitimate DO-001 message...")
        client.subscribe(TOPIC, qos=1)
    else:
        print("[ERROR] MQTT connection failed:", reason_code)

def on_message(client, userdata, msg):
    global original_payload, captured_sequence

    if captured.is_set():
        return

    try:
        data = json.loads(msg.payload.decode("utf-8"))

        if (
            data.get("sensor_id") != "DO-001"
            or "sequence" not in data
            or "hmac" not in data
        ):
            return

        original_payload = bytes(msg.payload)
        captured_sequence = data["sequence"]

        print("[CAPTURED] DO-001")
        print("Sequence:", captured_sequence)
        print("Value:", data.get("value"), "mg/L")

        captured.set()

    except (ValueError, UnicodeDecodeError) as exc:
        print("[SKIPPED]", exc)

client = mqtt.Client(

    client_id="AQ1-Demo-Replay"
)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    if not captured.wait(timeout=20):
        raise RuntimeError("No DO-001 message received within 20 seconds")

    # Stop receiving messages; keep MQTT connected for publishing.
    client.unsubscribe(TOPIC)

    print("[WAIT] Allowing gateway to process original message...")
    time.sleep(2)

    print("[REPLAY] Republishing sequence:", captured_sequence)

    result = client.publish(
        TOPIC,
        original_payload,
        qos=1,
        retain=False
    )
    result.wait_for_publish(timeout=10)

    if result.rc == mqtt.MQTT_ERR_SUCCESS and result.is_published():
        print("[SENT] Replay published successfully")
        print("[CHECK] Gateway should reject sequence:", captured_sequence)
    else:
        print("[ERROR] MQTT publish not confirmed:", result.rc)

finally:
    client.loop_stop()
    client.disconnect()

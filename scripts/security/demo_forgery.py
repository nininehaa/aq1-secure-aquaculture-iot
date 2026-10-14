import json
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPIC = "aquaculture/sensors/dissolved_oxygen"

message = {
    "sensor_id": "DO-001",
    "pond_id": "POND-01",
    "sensor_type": "dissolved_oxygen",
    "value": 1.0,
    "unit": "mg/L",
    "timestamp": int(time.time()),
    "sequence": 999999,
    "hmac": "0" * 64
}

print("=== AQ-1 SPOOFING ATTACK ===")
print("Attempting to inject false DO reading: 1.0 mg/L")
print("HMAC: deliberately invalid")

client = mqtt.Client(client_id="AQ1-Forgery-Demo")
client.connect(BROKER, 1883, 60)
client.loop_start()

result = client.publish(
    TOPIC,
    json.dumps(message),
    qos=1,
    retain=False
)
result.wait_for_publish(timeout=10)

print("MQTT publish result:", result.rc)
print("Attack message sent.")

time.sleep(1)
client.loop_stop()
client.disconnect()

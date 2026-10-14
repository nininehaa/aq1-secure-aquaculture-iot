import json
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPIC = "aquaculture/sensors/dissolved_oxygen"

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")

    print("\n=== CAPTURED DO-001 MESSAGE ===")
    print(payload)

    # Save exact message for replay testing
    with open("captured_do.json", "w") as f:
        f.write(payload)

    print("\nSaved to captured_do.json")
    client.disconnect()

client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)

print("Waiting for a DO-001 message...")
client.loop_forever()

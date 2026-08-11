import hashlib
import hmac
import json

import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883
TOPIC = "aquaculture/sensors/#"
SECRET_KEY = b"aq1-week5-secret-key"


def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))

        sensor_id = payload["sensor_id"]
        sensor_type = payload["sensor_type"]
        value = payload["value"]
        received_hmac = payload["hmac"]

        # Reconstruct the protected message.
        protected_message = f"{sensor_id}|{sensor_type}|{value}"

        # Calculate the expected HMAC.
        expected_hmac = hmac.new(
            SECRET_KEY,
            protected_message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        # Safely compare the received and expected signatures.
        if hmac.compare_digest(received_hmac, expected_hmac):
            print(
                f"ACCEPTED: {sensor_id} reported "
                f"{sensor_type} = {value} mg/L"
            )
            print("PASS: message integrity verified")
        else:
            print(
                f"REJECTED: integrity check failed for "
                f"message from {sensor_id}"
            )
            print("FAIL: message integrity check failed")

    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"REJECTED: invalid sensor payload ({error})")


client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print("Gateway is listening for authenticated sensor readings...")

client.loop_forever()
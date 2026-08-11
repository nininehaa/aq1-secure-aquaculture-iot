import time
import threading
from datetime import datetime
import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "aquaculture/sensors/#"

SENSOR_TIMEOUT = 10
last_message_time = None
outage_reported = False

def write_log(line):
    with open("sensor.log", "a") as file:
        file.write(line + "\n")

def on_message(client, userdata, message):
    global last_message_time, outage_reported

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value = message.payload.decode()

    last_message_time = time.time()
    outage_reported = False

    log_line = f"{timestamp} | {message.topic} | {value}"

    print(log_line)
    write_log(log_line)

def check_sensor_outage():
    global outage_reported

    while True:
        if last_message_time is not None:
            seconds_without_data = time.time() - last_message_time

            if seconds_without_data > SENSOR_TIMEOUT and not outage_reported:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                alert = (
                    f"{timestamp} | ALERT | SENSOR OUTAGE DETECTED | "
                    f"No valid reading for more than {SENSOR_TIMEOUT} seconds"
                )

                print(alert)
                write_log(alert)

                outage_reported = True

        time.sleep(1)

client = mqtt.Client()
client.on_message = on_message

client.connect(broker, port, 60)
client.subscribe(topic)

print("Monitoring started...")
print(f"Sensor outage timeout: {SENSOR_TIMEOUT} seconds")

thread = threading.Thread(
    target=check_sensor_outage,
    daemon=True
)
thread.start()

client.loop_forever()
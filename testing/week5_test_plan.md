\# Week 5 MQTT Test Plan



\## Test 1 - MQTT Broker

Action:

Start or confirm the Mosquitto broker is running.



Expected Result:

The broker is available on port 1883.



\## Test 2 - Dissolved Oxygen Sensor

Action:

Run the dissolved oxygen sensor simulator.



Expected Result:

A new dissolved oxygen reading is published approximately every 5 seconds.



\## Test 3 - Monitoring

Action:

Run monitor.py while the sensor is publishing.



Expected Result:

The monitoring script receives each MQTT reading and displays:

\- timestamp

\- MQTT topic

\- dissolved oxygen value



\## Test 4 - Log File

Action:

Allow the sensor and monitor to run for at least 30 seconds.



Expected Result:

Received readings are written to sensor.log with timestamps.



\## Test 5 - Sensor Stop

Action:

Stop do\_sensor.py using Ctrl + C.



Expected Result:

No new sensor readings are received by the monitoring script.



\## Test 6 - Sensor Restart

Action:

Start do\_sensor.py again.



Expected Result:

The monitoring script resumes receiving and logging dissolved oxygen readings.


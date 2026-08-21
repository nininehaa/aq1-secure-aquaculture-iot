# Sahil Basnet — Implementation Progress to Week 6

## My role in the project

My main responsibility in the AQ-1 project is the sensor, MQTT and network-security side of the system. So far I have mainly worked on the temperature sensor, MQTT communication, Mosquitto broker authentication, HMAC integrity protection, tamper testing and planning the GNS3 network scale-up.

The aim of my part is to make sure sensor data is sent through the system in a more secure way and that unauthorised clients or modified messages can be identified.

## 1. Temperature sensor simulator

I implemented the Python temperature sensor at:

`scripts/sensors/temperature_sensor.py`

The sensor represents a simulated aquaculture temperature sensor with:

- Sensor ID: `TEMP-001`
- Pond ID: `POND-01`
- MQTT topic: `aq1/pond1/temperature`

The sensor generates a temperature reading approximately every five seconds. It also gives the reading a simple status:

- below 25 C = `LOW`
- 25 C to 29 C = `NORMAL`
- above 29 C = `HIGH`

The message also includes the sensor ID, pond ID, sensor type, unit, timestamp and HMAC value.

## 2. MQTT communication

I used Eclipse Mosquitto as the MQTT broker for the current prototype.

The basic communication flow is:

```text
TEMP-001 temperature sensor
        |
        | publishes MQTT message
        v
Mosquitto broker
        |
        v
Authorised subscriber / monitoring component
```

The current local broker uses TCP port `1883`.

This is still a localhost-based prototype. The next network stage is to move the same working components into GNS3 so they communicate across separate virtual network nodes instead of all running on one computer.

## 3. MQTT authentication

I configured the temperature sensor to use MQTT username and password authentication.

The sensor reads the credentials from environment variables:

- `AQ1_MQTT_USERNAME`
- `AQ1_MQTT_PASSWORD`

I did this so the password does not need to be written directly inside the Python code.

The Mosquitto configuration disables anonymous access. The local Mosquitto password file is also excluded from GitHub using `.gitignore`.

### Authentication test

I tested the broker in two ways.

**Authorised test:**

I connected an MQTT subscriber using the configured credentials. The subscriber connected successfully and received live temperature messages.

**Unauthorised test:**

I then tried to connect without supplying a username or password.

The broker returned:

`Connection Refused: not authorised`

This confirmed that anonymous MQTT clients are blocked by the current broker configuration.

## 4. HMAC-SHA256 integrity protection

I added HMAC-SHA256 protection to the temperature sensor messages.

The HMAC secret is loaded from the environment variable:

`AQ1_TEMP_HMAC_KEY`

It is not stored directly in the committed Python source.

Before publishing a reading, the sensor builds the following string:

`sensor_id|pond_id|sensor_type|value|unit|status|timestamp`

It then generates an HMAC-SHA256 value from that string.

The purpose of this is message integrity. If one of the protected fields is changed after the HMAC is created, the verification result should no longer match.

HMAC does not hide or encrypt the temperature value. Its purpose in the current prototype is to help detect message modification.

## 5. Temperature tamper test

I also created a separate controlled tamper test at:

`scripts/security/temperature_tamper_test.py`

I kept this separate from the normal sensor so I could generate a repeatable malicious test message without changing the working temperature simulator.

The test works by:

1. creating a normal temperature reading
2. generating the correct HMAC for that reading
3. changing the temperature value and status after signing
4. keeping the original HMAC
5. publishing the modified message

Because the message is changed after signing, its contents no longer match its HMAC.

The team monitoring component now verifies the temperature HMAC using the same field order and rejects the tampered reading. This result is recorded in the Week 6 security test plan.

## 6. What I demonstrated

For the current local demo I can show the following parts of my implementation:

### Terminal 1 — Temperature sensor

This shows `TEMP-001` generating temperature readings, creating an HMAC and publishing the reading using authenticated MQTT.

### Terminal 2 — Authorised subscriber

This shows that an authorised MQTT client receives the actual JSON temperature messages through the broker.

### Terminal 3 — Broker status

This confirms that the Mosquitto broker is running and listening on port `1883`.

### Terminal 4 — Unauthorised connection test

This shows that a client without MQTT credentials is rejected by Mosquitto.

Together these terminals demonstrate the current sensor-to-broker security path.

## 7. Integration with the team

My temperature sensor publishes the protected message.

Neha's monitoring component verifies sensor messages, checks HMAC values and handles outage/recovery monitoring.

Arnob's area is the control and resilience side, including the planned `SAFE/HOLD` fail-safe behaviour.

The final project needs these areas to operate together as one end-to-end system.

## 8. Evidence in GitHub

Some of my main implementation commits are:

- `9a5216d` — `feat: add authenticated temperature sensor MQTT flow`
- `e98556c` — `feat: add HMAC protection and tamper test for temperature sensor`
- `fa4ac7c` — `feat: add HMAC integrity protection to temperature sensor`

Related team integration commits include:

- `283f698` — temperature HMAC verification and tamper rejection
- `816712f` — Week 6 security test-plan update

The Week 6 test plan also records the MQTT unauthorised-access test as PASS.

## 9. Current limitations

The current implementation is working as a local prototype, but it is not the final system yet.

The main remaining items for my area are:

- standardise the MQTT topic structure
- add topic-level MQTT access-control rules
- make the broker configuration more portable
- support secure monitor authentication to the broker
- add TLS for transport confidentiality
- move the sensor and broker onto separate GNS3 nodes
- create network segmentation and firewall rules
- capture MQTT traffic using Wireshark/GNS3 packet capture
- test the system across the virtual network instead of only localhost

## 10. Next step — GNS3

My next major task is to move the working local prototype into GNS3.

The first target path is:

```text
TEMP-001
   |
Pond A network
   |
Router / Firewall
   |
Mosquitto broker
   |
Monitoring component
```

Once this is working, the project can be expanded with additional pond networks, more sensors, an attacker/test network, monitoring services and the fail-safe control component.

The purpose of the GNS3 stage is to make the project closer to a real networked IoT environment rather than keeping every component on localhost.

## Documentation note

I am maintaining this file as my individual project documentation. I will keep updating it as I complete further implementation, testing, troubleshooting and GNS3 work.

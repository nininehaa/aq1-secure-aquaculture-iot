# Team Roles and Technical Ownership

## Project
Secure and Resilient IoT Sensor-Control System for Coral Coast Aquaculture

This document records the main technical responsibilities of each team member. The purpose is to make individual ownership clear while still showing how the components integrate as one system.

## Sahil Basnet — Sensor and Network Security

Sahil's current responsibility is the secure path from the simulated sensor to the MQTT infrastructure.

Main work areas:

- temperature sensor simulator `TEMP-001`
- MQTT publishing and subscribing
- Mosquitto broker configuration
- MQTT username/password authentication
- HMAC-SHA256 generation for temperature messages
- controlled temperature tamper testing
- broker and connection troubleshooting
- future MQTT ACL and TLS work
- GNS3 network segmentation and scale-up
- packet-capture and network-security testing

Current working producer path:

```text
TEMP-001 -> authenticated MQTT -> Mosquitto -> authorised subscriber/monitor
```

## Neha Thanait — Security Monitoring and Trust Validation

Neha's current responsibility is deciding whether received sensor data can be treated as trusted.

Main work areas:

- MQTT monitoring component
- dissolved-oxygen HMAC verification
- temperature HMAC verification
- rejection of invalid or malformed readings
- sensor outage detection
- recovery detection
- security event logging and alerts
- monitoring/dashboard security information

Current monitoring decision:

```text
Received sensor message
        |
        v
Integrity/format checks
        |
   +----+----+
   |         |
 valid     invalid
   |         |
 accept    reject + alert
```

## Md Monirul Haque Arnob — Control and Resilience

Arnob's main responsibility is the control response after sensor data has been classified as trusted or untrusted.

Main work areas:

- `SAFE/HOLD` control logic
- simulated aquaculture actuator behaviour
- Node-RED control integration
- response to invalid or unavailable trusted data
- controlled recovery after valid data returns
- resilience and broker/service failure handling

Current status: the fail-safe controller is still an integration task and should not be described as completed until it has been implemented and tested.

## Team Integration

The three areas connect as follows:

```text
Sahil
Sensor + MQTT/network security
        |
        v
Neha
Trust validation + monitoring
        |
        v
Arnob
Control response + SAFE/HOLD
```

No team member should claim another member's implementation as their own. Team documentation may describe the full system, but individual progress reports should identify the specific work completed by that student.

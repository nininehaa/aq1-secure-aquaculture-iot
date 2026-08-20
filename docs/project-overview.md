# Project Overview

## Project Title
Secure and Resilient IoT Sensor-Control System for Coral Coast Aquaculture

## Client
Coral Coast Aquaculture

## Team Members
- Neha Thanait
- Sahil Basnet
- Md Monirul Haque Arnob

## Project Scenario
AQ-1 — IoT/Sensor Security for a Prawn and Barramundi Farm

## Business Problem
Coral Coast Aquaculture depends on sensor information such as dissolved oxygen, water temperature, pH and feeder activity.

False, modified, spoofed or missing sensor readings could cause incorrect automated decisions and potentially harm farm operations or aquatic stock.

## Project Aim
The project aims to build and test a secure simulated aquaculture IoT system that protects:

- device/client identity
- sensor-message integrity
- sensor availability
- safe system behaviour when trusted data is unavailable

## Current Prototype

The current prototype includes:

- dissolved-oxygen and temperature sensor simulation
- Mosquitto MQTT communication
- authenticated MQTT access for the temperature path
- HMAC-based integrity protection
- temperature and dissolved-oxygen HMAC verification
- controlled tamper testing
- malformed-message rejection
- independent sensor outage detection
- sensor recovery detection

The `SAFE/HOLD` control layer and the larger GNS3 deployment remain integration work rather than completed implementation.

## Current System Flow

```text
Sensor simulators
      |
      v
Mosquitto MQTT broker
      |
      v
Security monitoring and HMAC verification
      |
      v
Trusted / rejected / outage state
      |
      v
SAFE/HOLD control integration
```

## Security Controls

### MQTT authentication
Controls whether a client is permitted to connect to the broker.

### HMAC-SHA256
Allows the monitoring component to detect changes to protected sensor-message fields.

### Availability monitoring
Detects when an expected sensor stops producing valid trusted readings.

### Fail-safe control
The intended final behaviour is to prevent unsafe automatic actions when trusted data is unavailable or invalid.

## Scale-Up Direction

The localhost prototype will be expanded into a GNS3-based virtual farm network with:

- multiple pond sensor networks
- routed network segments
- firewall/security rules
- separated monitoring and management networks
- an attacker/test network
- Wireshark packet-capture evidence
- later primary/backup MQTT broker testing
- Node-RED/dashboard and fail-safe control integration

See `docs/architecture/current-week6-architecture.md` for the current and planned architecture.

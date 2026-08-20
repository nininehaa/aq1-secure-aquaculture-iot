# Secure and Resilient IoT Sensor-Control System

## Client
Coral Coast Aquaculture

## Team Members
- Neha Thanait
- Sahil Basnet
- Md Monirul Haque Arnob

## Project Scenario
AQ-1 — IoT/Sensor Security for a Prawn and Barramundi Farm

## Project Overview
This project is building a simulated secure aquaculture IoT system for dissolved oxygen, temperature and other farm sensor readings.

The target system protects sensor identity, message integrity and service availability so that false, modified or missing sensor data does not blindly trigger unsafe control behaviour.

## Current Prototype Status

Implemented in the repository:

- Python dissolved-oxygen and temperature sensor simulation
- Eclipse Mosquitto MQTT messaging
- authenticated MQTT path for temperature sensor `TEMP-001`
- anonymous MQTT access disabled on the current secure broker configuration
- HMAC-SHA256 integrity generation for temperature readings
- HMAC verification for dissolved-oxygen and temperature readings
- controlled temperature tamper-test client
- rejection of tampered sensor messages by the monitoring logic
- independent sensor outage and recovery monitoring
- Week 6 security test plan

Current integration work still includes:

- MQTT authentication support for the monitoring client
- standardised MQTT topic structure and topic ACLs
- `SAFE/HOLD` fail-safe controller integration
- Node-RED/dashboard integration
- TLS and stronger key management
- GNS3 multi-pond network deployment and packet-capture testing

## Current Data Flow

```text
Sensor simulator
      |
      | MQTT + integrity-protected message
      v
Mosquitto MQTT broker
      |
      v
Security monitoring / verification
      |
      v
Trusted or rejected sensor state
      |
      v
SAFE/HOLD control integration (pending)
```

## Main Technologies

- Python
- Eclipse Mosquitto MQTT
- HMAC-SHA256
- GitHub and GitHub Projects
- Microsoft Teams
- Wireshark
- GNS3 for planned network-scale deployment
- Node-RED for planned monitoring/control integration

## Team Technical Focus

- **Sahil Basnet:** sensor/MQTT/network security, temperature producer, broker authentication, HMAC generation, tamper testing, GNS3 network scale-up
- **Neha Thanait:** sensor trust validation, HMAC verification, outage/recovery monitoring, security logging/alerts
- **Md Monirul Haque Arnob:** control/resilience integration, `SAFE/HOLD`, Node-RED and simulated actuator behaviour

## Documentation

- [Project overview](docs/project-overview.md)
- [Initial architecture](docs/architecture/system-architecture.md)
- [Current Week 6 architecture and GNS3 direction](docs/architecture/current-week6-architecture.md)
- [Security threat model](docs/security/threat-model.md)
- [Temperature MQTT security design](docs/security/temperature-mqtt-security.md)
- [Sahil Week 6 implementation progress](docs/progress/sahil-week6-progress.md)
- [Week 6 security test plan](testing/Week_6_Security_Test_Plan.md)

## Demonstration Goals

1. An authorised sensor publishes a valid reading.
2. An authorised subscriber/monitor receives the reading.
3. A client without valid MQTT credentials is rejected.
4. A tampered sensor message fails integrity verification.
5. A sensor outage is detected independently.
6. The integrated control system ultimately enters `SAFE/HOLD` when trusted data is unavailable or invalid.

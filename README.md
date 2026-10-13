# AQ-1 Secure and Resilient IoT Sensor-Control System

## Client
Coral Coast Aquaculture

## Team Members
- Neha Thanait
- Sahil Basnet
- Md Monirul Haque Arnob

## 1. Project Overview

AQ-1 is a cybersecurity capstone project developed to demonstrate how IoT sensor data can be secured and monitored in an aquaculture environment.

Aquaculture farms depend on water-quality measurements such as dissolved oxygen (DO), pH and temperature to maintain suitable conditions for fish and prawns.

If an attacker modifies sensor readings, impersonates a legitimate sensor or replays old messages, the system may receive misleading information and make unsafe decisions.

Our project demonstrates how sensor messages can be verified before being trusted and how the monitoring system responds to malicious or unavailable data.

The main cybersecurity objectives are:

- **Integrity:** Detect modified sensor readings using HMAC-SHA256.
- **Authenticity:** Verify messages using sensor identity and shared cryptographic keys.
- **Availability:** Detect missing or interrupted sensor readings.
- **Replay protection:** Reject previously processed messages using sequence numbers and freshness checks.
- **Fail-safe monitoring:** Demonstrate logical SAFE/HOLD responses when trusted sensor information is unavailable.

## 2. Sensor Implementation

Our project combines simulated aquaculture sensors with a physical IoT temperature sensor.

| Sensor | Implementation | Purpose |
|---|---|---|
| Dissolved oxygen (DO) | Simulated in GNS3 | Generate oxygen readings for security monitoring and attack demonstrations |
| pH | Simulated in GNS3 | Generate water pH readings within the virtual farm environment |
| Temperature | Physical DS18B20 sensor connected to ESP32-C3 | Collect real temperature measurements and transmit them to the GNS3 gateway |

The physical temperature sensor was programmed using Arduino IDE and successfully communicated with the gateway through HiveMQ MQTT.

The DO and pH sensors were simulated rather than physically deployed.

## 3. System Architecture

The AQ-1 system connects simulated farm sensor nodes with a physical IoT temperature sensor through MQTT communication and a security gateway.

### Overall Architecture

```text
Physical DS18B20 Temperature Sensor
               |
               v
            ESP32-C3
          (Arduino IDE)
               |
               v
       HiveMQ MQTT Broker
               |
               v
       GNS3 Python Gateway <---- Simulated DO Sensor
               |           <---- Simulated pH Sensor
               |
               | <--------- GNS3 Attacker Node
               v
       Security Verification
       - HMAC validation
       - Sensor identity checks
       - Sequence/replay checks
       - Availability monitoring
               |
               v
       Verified Sensor Data
       Security Events / Alerts
               |
               v
       Arnob's Node-RED Dashboard
               |
               +---- Sensor Monitoring
               +---- Security Alerts
               +---- Controller Status
               |
               v
       Logical NORMAL / SAFE-HOLD
```

The GNS3 environment was used to simulate networked aquaculture components, integrate sensor communication and demonstrate cybersecurity attacks.

The physical sensor communicated through the public HiveMQ broker, and its readings were received and verified by the GNS3 gateway.

## 4. Physical Temperature Sensor Integration

Neha and Sahil worked together on the physical temperature sensor implementation.

### Hardware Used

- ESP32-C3 microcontroller
- DS18B20 temperature sensor
- Breadboard and jumper wires
- 4.7 kΩ pull-up resistor
- USB connection for programming

### Software and Communication

- Arduino IDE
- HiveMQ MQTT broker
- Python-based GNS3 gateway

The DS18B20 collected actual temperature readings. The ESP32-C3 processed these measurements and published sensor messages using MQTT.

The gateway subscribed to the temperature topic:

`aq1/pond1/temperature`

The gateway received the sensor readings and performed security verification.

This integration demonstrated how physical IoT measurements could be incorporated into a virtualised cybersecurity environment.

## 5. Cybersecurity Implementation

### HMAC-SHA256 Verification

The project uses HMAC-SHA256 to check whether sensor messages have been modified.

The sender generates an HMAC using a shared secret key and the agreed message contents.

The gateway recalculates the expected HMAC and compares it with the received value.

Valid messages are accepted, while messages with incorrect HMAC values are rejected.

HMAC provides message integrity and authentication, but it does not encrypt the data.

### Replay Protection

Replay attacks occur when an attacker resends an earlier legitimate message.

Because a replayed message may contain a valid HMAC, the gateway also checks message sequence numbers and freshness information where supported by the sensor pathway.

Messages identified as duplicates or stale are rejected instead of being treated as new measurements.

### Sensor Availability Monitoring

The system monitors the arrival of valid sensor readings.

If a previously active sensor stops providing valid data beyond the configured timeout, an outage warning can be generated.

This is important because the absence of sensor data should not be treated as proof that water conditions remain safe.

### Logical SAFE/HOLD Response

The project demonstrates software-based supervisory control states.

- **NORMAL:** Trusted sensor readings are available for monitoring.
- **SAFE/HOLD:** The system identifies unavailable or untrusted information and indicates that normal automatic decisions should not continue.

The SAFE/HOLD response is part of the project's cybersecurity and monitoring logic.

**The project did not implement or operate a physical pump, aerator or relay.**

## 6. Cybersecurity Attack Demonstrations

The project uses a controlled attacker node within the GNS3 environment to demonstrate three main cybersecurity threats.

| Attack | Description | Security response |
|---|---|---|
| Spoofing | The attacker pretends to be a legitimate sensor and publishes a forged message | Invalid authentication or HMAC causes rejection |
| Tampering | The attacker changes a sensor reading without creating a matching valid HMAC | The gateway rejects the modified message |
| Replay | The attacker retransmits a previously valid sensor message | Sequence-number checks identify and reject the repeated message |

These scenarios demonstrate why sensor information must be authenticated and checked before it is used for monitoring or control decisions.

## 7. Node-RED Dashboard

The final project demonstration used ** Node-RED dashboard**.

The dashboard provides a visual interface for monitoring aquaculture sensor information and security events.

Its functions include:

- Displaying temperature and simulated water-quality readings
- Presenting sensor status and availability
- Showing security warnings
- Displaying accepted or rejected message information
- Presenting logical control states
- Supporting interpretation of sensor outages and cybersecurity events

The gateway performs the security verification, while Node-RED presents relevant information to the user.

The project also used SQLite as part of its monitoring and data-storage environment.

## 8. Project Development

### Stage 1 — Python and MQTT Prototype

The initial project used Python sensor simulators and Eclipse Mosquitto MQTT.

This helped establish:

- MQTT publishing and subscribing
- Dissolved oxygen and temperature message formats
- HMAC generation and verification
- Tampered-message rejection
- Sensor outage and recovery detection
- Security event logging

These initial development files remain in the repository as historical prototype evidence.

### Stage 2 — GNS3 Network Development

Following feedback about project scale, the team expanded the implementation into GNS3.

This involved:

- Building and configuring virtual network components
- Simulating dissolved oxygen and pH sensors
- Configuring network communication
- Integrating the Python security gateway
- Testing normal and malicious sensor traffic
- Troubleshooting virtual machines, network adapters and connectivity

### Stage 3 — Physical ESP32 Temperature Sensor

The team integrated an actual DS18B20 temperature sensor with an ESP32-C3.

The ESP32-C3 used HiveMQ to transmit physical sensor readings, which were successfully received by the GNS3 gateway.

### Stage 4 — Dashboard and Security Demonstration

The system was connected with Arnob's Node-RED dashboard for monitoring sensor readings, security alerts and logical control states.

The team prepared demonstrations involving legitimate data, spoofing, tampering, replay attacks and sensor availability.

## 9. Main Technologies

- Python
- GNS3
- HiveMQ MQTT Broker
- Eclipse Mosquitto MQTT (initial prototype)
- HMAC-SHA256
- ESP32-C3 microcontroller
- DS18B20 temperature sensor
- Arduino IDE
- Node-RED dashboard
- SQLite
- Git and GitHub

## 10. Team Contributions

### Sahil Basnet

Worked on sensor communication, MQTT and network security, GNS3 integration, and the physical ESP32 temperature-sensor implementation with Neha.

### Neha Thanait

Worked on security monitoring, HMAC verification, sensor outage and recovery detection, security alerts, testing, documentation, GNS3 troubleshooting and the physical temperature-sensor implementation with Sahil.

### Md Monirul Haque Arnob

Worked on GNS3 integration, the Node-RED dashboard and monitoring/control components, including logical SAFE/HOLD behaviour.


## 11. Testing and Demonstration

The project involved testing and demonstrating:

1. Valid sensor readings being received and accepted
2. Physical temperature readings reaching the GNS3 gateway through HiveMQ
3. HMAC verification
4. Rejection of spoofed sensor messages
5. Rejection of tampered sensor messages
6. Detection of replayed messages
7. Sensor outage detection
8. Logical SAFE/HOLD warning states
9. Display of sensor and security information in Node-RED

Earlier prototype testing is documented in:

- `testing/Week_6_Security_Test_Plan.md`
- `testing/security-test-results.md`
- `docs/evidence/`
- `docs/gns3/`

Final GNS3 and physical-device evidence should be documented separately from the earlier prototype results.

## 12. Limitations and Future Improvements

AQ-1 is an academic cybersecurity prototype, not a production-ready aquaculture control system.

Current limitations and future improvements include:

- Stronger cryptographic key management
- TLS-secured MQTT communication
- Improved broker authentication and access control
- Consistent replay protection across every sensor pathway
- More comprehensive testing of network failures
- Additional physical DO and pH sensors
- More reliable persistent monitoring storage and recovery procedures
- Physical pump or aerator integration
- Further testing under real aquaculture operating conditions

The public HiveMQ broker used in the demonstration communicates over port 1883 without MQTT transport encryption.

The project demonstrates security concepts and software responses, but does not claim to have deployed a fully automated physical farm-control system.

## 13. Key Project Outcome

The main outcome of AQ-1 is demonstrating why IoT sensor readings should be verified before being trusted.

The project combines simulated dissolved oxygen and pH sensors, a physical ESP32 temperature sensor, MQTT communication, a GNS3 security gateway, attack demonstrations and Node-RED monitoring.

This shows how cybersecurity principles can help protect aquaculture systems from misleading sensor information and support safer monitoring decisions.

## 14. Project Documentation
- [Final Showcase Evidence](docs/evidence-index.md)
- [Final Demonstration Screenshots](docs/evidence/final-showcase/)
- [Physical ESP32-C3 Temperature Sensor Code](hardware/esp32-temperature/)
- [Project Plan](docs/project-management/project-plan.md)
- [Implementation Status](docs/project-management/implementation-status.md)
- [Team Roles](docs/team-roles.md)
- [Documentation Index](docs/README.md)
- [Requirements Traceability](docs/project-management/requirements-traceability.md)
- [Security Test Results](testing/security-test-results.md)
- [AI Use Log](AI-log.md)

Features should only be marked complete when supported by implementation, testing and evidence.

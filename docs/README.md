# AQ-1 Project Documentation

**Project:** AQ-1 Secure and Resilient IoT Sensor-Control System  
**Client:** Coral Coast Aquaculture  
**Course:** COIT13236 Cyber Security Project  
**Team:** Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob

## 1. Documentation Overview

This folder contains the technical, security, implementation and project-management documentation for AQ-1.

The project developed from an initial Python and MQTT prototype into an integrated cybersecurity demonstration using:

- Simulated dissolved oxygen (DO) and pH sensors in GNS3.
- A physical DS18B20 temperature sensor connected to an ESP32-C3.
- HiveMQ for transmitting physical temperature readings.
- A Python security gateway running in GNS3.
- HMAC-SHA256 integrity verification and replay detection.
- Controlled spoofing, tampering and replay demonstrations.
- A Node-RED dashboard for monitoring sensor information and security events.
- Logical NORMAL and SAFE/HOLD control states.

The project did not include physical pump, aerator or relay operation.

## 2. Start Here

These documents provide the main overview of the project.

1. [Main Project README](../README.md) — Project summary, architecture, technologies and outcomes.
2. [Project Overview](project-overview.md) — Business problem, objectives and final implementation.
3. [Project Plan](project-management/project-plan.md) — Development phases, implementation scope and remaining tasks.
4. [Implementation Status](project-management/implementation-status.md) — Demonstrated components, limitations and documentation still required.
5. [Team Roles and Collaboration](team-roles.md) — Technical responsibilities and collaborative development.
6. [Requirements Traceability](project-management/requirements-traceability.md) — Requirements, implementation and testing.
7. [Final System Architecture](architecture/system-architecture.md) — Logical system components and communication.
8. [Security Design](security/security-design.md) — Cybersecurity threats, controls and attack demonstrations.

## 3. Final System Overview

The completed academic demonstration combines simulated aquaculture sensor information with real physical temperature measurements.

### Sensor Implementation

| Sensor | Implementation |
|---|---|
| Dissolved oxygen | Simulated in GNS3 |
| pH | Simulated in GNS3 |
| Temperature | Physical DS18B20 sensor connected to ESP32-C3 |

### Communication and Monitoring

```text id="d5w4sm"
Physical DS18B20 Sensor
          |
        ESP32-C3
          |
          v
     HiveMQ Broker
          |
          v
     GNS3 Gateway <--- Simulated DO Sensor
          ^        <--- Simulated pH Sensor
          |
     Attacker Node
          |
          v
   Security Verification
          |
          v
   Sensor Data and Alerts
          |
          v
    Node-RED Dashboard
          |
          v
   Logical NORMAL / SAFE-HOLD
```

The gateway receives messages and performs security checks before readings are treated as trusted.

Node-RED is the final monitoring dashboard.

Node-RED was used for the final showcase; the unused Azure implementation has been removed from the current repository.

## 4. Architecture and Design Documents

### Final Architecture

- [System Architecture](architecture/system-architecture.md) — Final GNS3, physical sensor and dashboard architecture.
- [Security Design](security/security-design.md) — Security controls, message verification and attack handling.

### Earlier Architecture and Design

These files document the project's development and initial technical decisions:

- [Week 6 Architecture](architecture/current-week6-architecture.md)
- [Sensor, MQTT and Network Security Design](design/sensor-mqtt-network-security-design.md)
- [Monitoring and Trust Validation Design](design/monitoring-trust-validation-design.md)
- [Design Documentation](design/design%20documentation.md)

Earlier designs should be treated as historical development records where they differ from the final implementation.

## 5. GNS3 Documentation

The GNS3 environment provided the virtual network used for simulated sensors, gateway communication and controlled security testing.

Existing documentation:

- [GNS3 Design](gns3/gns3-design.md)
- [Network Addressing](gns3/network-addressing.md)
- [Week 7 Temperature and Monitoring Validation](gns3/week7-temp-monitor-validation.md)

The final GNS3 implementation should be documented using the actual final topology, network settings and scripts.

Earlier GNS3 documents may describe configurations used during development rather than the final showcase.

## 6. Sensor and Monitoring Implementation

### Initial Python Prototype

The original prototype used Python sensor programs and Eclipse Mosquitto MQTT.

Relevant repository files include:

- [Dissolved Oxygen Sensor](../scripts/sensors/do_sensor.py)
- [Temperature Sensor Prototype](../scripts/sensors/temperature_sensor.py)
- [Security Monitor](../scripts/monitoring/monitor.py)
- [Initial Gateway](../scripts/gateway/gateway.py)
- [Dissolved Oxygen Implementation Notes](implementation/dissolved-oxygen-sensor.md)
- [Monitoring Implementation Notes](implementation/monitoring.md)

These files provide historical implementation context.

They should not automatically be described as the exact scripts running in the final GNS3 showcase.

### Physical Temperature Integration

The final physical temperature pathway was:

`DS18B20 → ESP32-C3 → HiveMQ → GNS3 Gateway`

The physical sensor was programmed using Arduino IDE.

The [Arduino sketch, setup notes and safe configuration template](../hardware/esp32-temperature/) are available. The [showcase evidence index](evidence-index.md) links the physical sensor photographs and test results.

## 7. Cybersecurity Testing

The project focused on verifying incoming sensor data and detecting malicious messages.

### Main Attack Demonstrations

| Attack | Security objective |
|---|---|
| Spoofing | Detect forged sensor messages |
| Tampering | Detect modified data through HMAC verification |
| Replay | Detect previously processed messages through sequence-number checks |

### Earlier Test Documentation

- [Week 5 Test Plan](../testing/week5_test_plan.md)
- [Week 6 Security Test Plan](../testing/Week_6_Security_Test_Plan.md)
- [Security Test Results](../testing/security-test-results.md)

These documents record earlier project testing.

The final GNS3 attack results should be documented separately, including the actual commands, gateway responses and observed outcomes.

## 8. Node-RED Dashboard and Logical Control

The final showcase used Arnob's Node-RED dashboard.

The dashboard was used to present sensor information, security alerts and logical control-state information.

The project demonstrated software-based NORMAL and SAFE/HOLD states.

No physical pump, aerator or relay was operated.

The final Node-RED flow export and dashboard screenshots should be included in the repository to support reproducibility.

## 9. Project Management

The following documents record project decisions and progress:

- [Project Plan](project-management/project-plan.md)
- [Implementation Status](project-management/implementation-status.md)
- [Requirements Traceability](project-management/requirements-traceability.md)
- [Risk Register](project-management/risk-register.md)
- [Project Decisions](project-decisions.md)
- [Weekly Review Template](project-management/weekly-review-template.md)
- [Troubleshooting](troubleshooting.md)

These documents should be kept consistent with the final project scope.

## 10. Development Progress Records

The repository contains progress records from earlier stages:

- [Week 5 Progress](progress/week-5.md)
- [Week 6 Progress](progress/week-6.md)
- [Week 7 Progress](progress/week-7.md)
- [Week 8 Progress](progress/week-8.md)

These documents record how the project developed over time and should not be rewritten to suggest that later functionality existed in earlier weeks.

The repository was used collaboratively. Uploading a file or creating a commit does not necessarily mean that a single person exclusively developed that component.

## 11. Project Evidence Index

- [Evidence Index](evidence-index.md)

This file should distinguish between:

- Earlier Python and MQTT prototype results.
- GNS3 network and cybersecurity demonstrations.
- Physical ESP32 temperature-sensor integration.
- Node-RED monitoring and logical control.
- Final documentation and configuration still to be consolidated.

## 12. Remaining Repository Organisation

The following final artefacts should be added or linked when available:

- Final GNS3 project and topology.
- Final Python gateway script.
- GNS3 dissolved oxygen and pH scripts.
- Attacker-node scripts for spoofing, tampering and replay.
- ESP32-C3 Arduino sketch.
- HiveMQ and GNS3 integration instructions.
- Node-RED flow export.
- Final security test results.
- Dashboard and demonstration screenshots.
- Startup and troubleshooting instructions.

Files containing passwords, HMAC secret keys or private credentials must not be committed.

## 13. Historical and Superseded Components

The repository retains the early Python and MQTT prototype for development history. The unused Azure dashboard files have been removed from the current branch.

These records may be retained as historical development material but should not be confused with the final Node-RED implementation.

Any decision to archive or remove outdated files should be made after checking that they are not required for project history or assessment records.

## 14. Documentation Principles

Project documentation should accurately distinguish:

- What was planned.
- What was implemented.
- What was demonstrated.
- What was tested.
- What remains to be documented.
- What was outside the implemented scope.

The team's technical work should be described collaboratively, while maintaining clarity about the functions of each component.

## 15. Project Outcome

AQ-1 demonstrates how simulated aquaculture sensors and physical IoT hardware can be integrated with cybersecurity verification and dashboard monitoring.

The project highlights the importance of message integrity, replay detection, sensor availability and logical safe-control responses when handling aquaculture sensor information.

The documentation supports understanding, reviewing and reproducing the team's academic cybersecurity implementation.

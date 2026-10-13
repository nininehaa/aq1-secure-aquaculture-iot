# AQ-1 Project Evidence Index

**Project:** AQ-1 Secure and Resilient IoT Sensor-Control System  
**Client:** Coral Coast Aquaculture  
**Course:** COIT13236 Cyber Security Project  
**Team:** Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob

## 1. Purpose

This document provides an organised overview of the technical implementation, testing and supporting materials developed throughout the AQ-1 project.

The project evolved from an initial Python and MQTT prototype into a GNS3-based cybersecurity demonstration integrating physical and simulated sensors, security verification and Node-RED monitoring.

This index distinguishes between earlier prototype materials, functionality demonstrated in the final showcase and technical files that still need to be consolidated in GitHub.

The repository is a collaborative team workspace. The person who uploads a file is not necessarily its sole developer.

## 2. Final Project Components

| Component | Implementation | Status |
|---|---|---|
| Dissolved oxygen sensor | Simulated in GNS3 | Demonstrated |
| pH sensor | Simulated in GNS3 | Demonstrated |
| Temperature sensor | Physical DS18B20 connected to ESP32-C3 | Demonstrated |
| Physical MQTT communication | ESP32-C3 → HiveMQ → GNS3 gateway | Demonstrated |
| Security gateway | Python gateway running within GNS3 | Demonstrated |
| HMAC-SHA256 integrity verification | Gateway security validation | Demonstrated |
| Spoofing detection | Controlled attacker-node test | Demonstrated |
| Tampering detection | Controlled attacker-node test | Demonstrated |
| Replay detection | Sequence-number checking in tested GNS3 pathway | Demonstrated |
| Sensor outage and recovery | Timeout-based monitoring | Tested in earlier prototype; final records to be consolidated |
| Node-RED dashboard | Monitoring and visualisation | Demonstrated |
| Logical NORMAL and SAFE/HOLD | Software-based control states | Demonstrated |
| Physical pump or relay control | Not implemented | Outside scope |
| Azure dashboard | Earlier implementation experiment | Not used in final showcase |

A component being demonstrated does not automatically mean its final source code, configuration and screenshots are already present in GitHub.

## 3. Current GitHub Documentation

### Project Information

- [Main README](../README.md)
- [Project Overview](project-overview.md)
- [Project Plan](project-management/project-plan.md)
- [Implementation Status](project-management/implementation-status.md)
- [Team Roles](team-roles.md)
- [Requirements Traceability](project-management/requirements-traceability.md)

### Architecture and Security

- [System Architecture](architecture/system-architecture.md)
- [Security Design](security/security-design.md)
- [Threat Model](security/threat-model.md)
- [GNS3 Design](gns3/gns3-design.md)
- [Network Addressing](gns3/network-addressing.md)

These documents explain the system architecture, cybersecurity objectives and relevant design decisions.

Historical documents may describe earlier configurations rather than the final showcase.

## 4. Initial Python and MQTT Prototype

The team initially used Python-based sensor simulations and Eclipse Mosquitto MQTT.

Relevant source files include:

- [Dissolved Oxygen Sensor](../scripts/sensors/do_sensor.py)
- [Temperature Sensor Prototype](../scripts/sensors/temperature_sensor.py)
- [Security Monitor](../scripts/monitoring/monitor.py)
- [Initial Gateway](../scripts/gateway/gateway.py)

### Recorded Prototype Testing

- [Week 5 Test Plan](../testing/week5_test_plan.md)
- [Week 6 Security Test Plan](../testing/Week_6_Security_Test_Plan.md)
- [Security Test Results](../testing/security-test-results.md)

The earlier prototype tested MQTT communication, HMAC verification, modified-message rejection, sensor outage detection and recovery behaviour.

These records show how the team developed and validated the project's initial cybersecurity functionality.

They should not be treated as the complete final GNS3 implementation.

## 5. GNS3 Implementation

GNS3 was used to build the virtual aquaculture environment.

The final demonstration incorporated:

- Simulated dissolved oxygen readings.
- Simulated pH readings.
- A Python security gateway.
- Communication between relevant virtual components.
- Controlled attacker-node demonstrations.
- Integration of physical temperature readings through HiveMQ.
- Monitoring and logical control-state information.

### Existing GNS3 Documentation

- [GNS3 Design](gns3/gns3-design.md)
- [Network Addressing](gns3/network-addressing.md)

### Final GNS3 Artefacts to Consolidate

- Final project export or topology.
- Actual virtual node configurations.
- Final Python gateway code.
- Simulated DO and pH sensor programs.
- Network configuration and startup instructions.
- Screenshots or logs confirming final connectivity.

These should be recorded using the actual settings from the working showcase environment rather than values from earlier design proposals.

## 6. Physical ESP32 Temperature Sensor

The physical temperature-sensing implementation used:

- ESP32-C3 microcontroller.
- DS18B20 temperature sensor.
- Arduino IDE.
- HiveMQ MQTT broker.

### Physical Sensor Data Flow

```text
DS18B20 Temperature Sensor
             |
             v
          ESP32-C3
             |
             v
        HiveMQ Broker
             |
             v
        GNS3 Gateway
             |
             v
      Security Monitoring
```

The team successfully received physical temperature readings at the GNS3 gateway through HiveMQ.

### Physical Sensor Implementation Evidence

The final ESP32-C3 physical temperature sensor firmware has been uploaded to GitHub.

**Available files:**
- [Final Arduino sketch](../hardware/esp32-temperature/AQ1_Physical_Temperature_HMAC.ino)
- [Physical sensor README](../hardware/esp32-temperature/README.md)
- [Safe configuration template](../hardware/esp32-temperature/secrets.example.h)

The physical temperature sensor implementation was developed and tested collaboratively by Sahil Basnet and Neha Thanait. The ESP32-C3 publishes DS18B20 temperature measurements to the HiveMQ MQTT broker, where the GNS3 gateway receives and verifies signed messages.

**Additional evidence to consolidate:**
- Hardware wiring diagram and photographs.
- Gateway reception and HMAC verification screenshots.
- Final demonstration evidence linked to the submitted report.

Real Wi-Fi passwords and HMAC secret keys are not included in the uploaded configuration template.

## 7. Cybersecurity Attack Testing

Three primary attacks were demonstrated within the GNS3 environment.

| Test | Attack behaviour | Expected security result |
|---|---|---|
| Spoofing | Submit a forged sensor message | Invalid message rejected |
| Tampering | Change a protected sensor reading | HMAC mismatch detected |
| Replay | Resend a previously valid sensor message | Repeated sequence number rejected |

### Supporting Results to Consolidate

For each attack, record:

1. The attack scenario and purpose.
2. Which simulated sensor identity was used.
3. How the controlled attack was executed.
4. The gateway response.
5. Whether the test passed.
6. The relevant screenshot, log or script.

The final attack evidence should be recorded separately from the earlier Week 6 prototype tests.

## 8. Node-RED Dashboard

The final AQ-1 demonstration used the Node-RED dashboard developed as part of the team's integrated GNS3 environment.

The dashboard presents sensor information, monitoring events, security alerts and logical control status.

### Artefacts to Consolidate

- Node-RED flow export.
- Dashboard screenshots.
- Gateway-to-dashboard communication configuration.
- Logical NORMAL and SAFE/HOLD demonstration results.
- Relevant monitoring or data-storage configuration.

The older Azure dashboard code does not represent the final showcase dashboard.

## 9. Logical Control

AQ-1 demonstrates software-based supervisory control states.

### NORMAL

Indicates that the monitoring system has acceptable trusted sensor information.

### SAFE/HOLD

Indicates that unreliable or unavailable information requires a safety-oriented supervisory response.

These are logical states, not evidence of physical actuator operation.

No physical pump, aerator or relay was implemented or operated.

## 10. Project Progress and Management Records

The repository includes project-management and earlier progress documentation:

- [Project Decisions](project-decisions.md)
- [Risk Register](project-management/risk-register.md)
- [Week 5 Progress](progress/week-5.md)
- [Week 6 Progress](progress/week-6.md)
- [Week 7 Progress](progress/week-7.md)
- [Week 8 Progress](progress/week-8.md)
- [AI Use Log](../AI-log.md)

These documents provide historical context and should retain the chronological development of the project.

## 11. Outstanding Repository Tasks

The remaining repository organisation tasks include:

- Consolidating the final GNS3 project and source files.
- Adding the ESP32 Arduino sketch.
- Adding the final Node-RED flow.
- Documenting actual final MQTT topic names and sensor identifiers.
- Recording final security attack outcomes.
- Correcting outdated historical document descriptions.
- Reviewing the older Azure dashboard files and workflow.
- Updating setup instructions so the final demonstration can be reproduced.
- Checking that documentation links point to existing files.

These tasks relate primarily to the completeness and consistency of the repository, rather than implying that the corresponding features were not demonstrated.

## 12. Security of Repository Contents

The project repository should not contain:

- MQTT passwords.
- HiveMQ credentials.
- HMAC secret keys.
- Azure or other service tokens.
- Private certificates or keys.
- Other confidential configuration information.

Use placeholder values in documentation and environment variables or appropriately protected local configuration for sensitive values.

## 13. Team Collaboration

AQ-1 was developed collaboratively by Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob.

The team contributed to planning, implementation, configuration, troubleshooting, testing and integration.

GitHub was used to maintain shared project materials. Individual uploads or commits do not necessarily establish exclusive authorship of a particular component.

The main purpose of this evidence index is to document the project's technical functionality and results.

## 14. Summary

AQ-1 demonstrates the integration of simulated aquaculture sensors, a physical IoT temperature sensor, MQTT communication, GNS3 cybersecurity verification and Node-RED monitoring.

Its principal cybersecurity demonstrations involve HMAC-based integrity checking, spoofing and tampering detection, replay protection and logical safe-control responses.

This index connects the project documentation with the implementation and testing materials needed to understand and reproduce the academic demonstration.

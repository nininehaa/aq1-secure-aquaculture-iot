# AQ-1 Requirements and Traceability Matrix

**Project:** AQ-1 Secure and Resilient IoT Sensor-Control System  
**Client:** Coral Coast Aquaculture  
**Course:** COIT13236 Cyber Security Project  
**Updated:** 13 October 2026

## 1. Purpose

This document maps the cybersecurity and IoT requirements of AQ-1 to the system implementation, testing activities and documentation.

AQ-1 was developed collaboratively by Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob.

The final demonstration combines simulated dissolved oxygen and pH sensors, a physical ESP32-C3 temperature sensor, MQTT communication, a GNS3 security gateway, controlled cybersecurity attacks and a Node-RED dashboard.

The matrix distinguishes between functionality demonstrated by the team and final artefacts that still need to be consolidated in GitHub.

## 2. Requirement Status Definitions

- **Demonstrated:** Functionality was shown in the integrated project environment.
- **Implemented:** Working functionality exists, but full final demonstration evidence may still need documenting.
- **Partially validated:** Functionality was tested in the earlier prototype or only part of the final system.
- **Documentation pending:** Functionality has been demonstrated, but final files or test records have not yet been added to GitHub.
- **Outside scope:** Functionality was not part of the completed implementation.

## 3. Functional and Security Requirements

| ID | Requirement | Implementation | Current status |
|---|---|---|---|
| R-01 | Generate dissolved oxygen readings | Simulated DO sensor in GNS3 | Demonstrated |
| R-02 | Generate pH readings | Simulated pH sensor in GNS3 | Demonstrated |
| R-03 | Collect physical temperature readings | DS18B20 connected to ESP32-C3 | Demonstrated |
| R-04 | Transmit physical sensor data through MQTT | ESP32-C3 to HiveMQ | Demonstrated |
| R-05 | Integrate physical data with virtual farm network | HiveMQ to GNS3 gateway | Demonstrated |
| R-06 | Verify sensor-message integrity | HMAC-SHA256 gateway verification | Demonstrated |
| R-07 | Detect spoofed sensor messages | GNS3 attacker demonstration | Demonstrated |
| R-08 | Detect tampered sensor readings | HMAC mismatch checking | Demonstrated |
| R-09 | Detect replayed messages | Gateway sequence-number checks | Demonstrated for tested GNS3 pathway |
| R-10 | Monitor missing or interrupted sensor data | Timeout-based monitoring | Implemented in earlier prototype; final validation to be documented |
| R-11 | Display aquaculture readings and security information | Node-RED dashboard | Demonstrated |
| R-12 | Demonstrate logical safety-control states | NORMAL and SAFE/HOLD | Demonstrated |
| R-13 | Support physical pump or aerator operation | Not implemented | Outside scope |
| R-14 | Document and reproduce the final system | GitHub documentation and final setup files | In progress |

## 4. Security Test Requirements

| Test ID | Security test | Expected result | Reported outcome |
|---|---|---|---|
| ST-01 | Submit a legitimate sensor reading | Gateway accepts valid information | Demonstrated |
| ST-02 | Send a message with an invalid HMAC | Gateway rejects the message | Demonstrated |
| ST-03 | Impersonate a trusted sensor | Forged message rejected | Demonstrated |
| ST-04 | Modify a reading after signing | HMAC verification fails | Demonstrated |
| ST-05 | Replay a previously valid message | Duplicate sequence rejected | Demonstrated |
| ST-06 | Stop valid sensor messages | Monitoring detects an outage | Tested in earlier prototype |
| ST-07 | Restore valid sensor messages | Monitoring identifies recovery | Tested in earlier prototype |
| ST-08 | Transmit actual temperature readings | GNS3 gateway receives readings through HiveMQ | Demonstrated |
| ST-09 | Display sensor and security information | Node-RED displays relevant information | Demonstrated |
| ST-10 | Trigger a logical safety response | SAFE/HOLD state shown | Demonstrated |
| ST-11 | Operate a physical pump | Not applicable | Not implemented |

Final test logs and screenshots should be linked to these test IDs when the team's demonstration files are consolidated.

## 5. System Integration

The integrated system uses the following data flow:

```text
Physical DS18B20 Temperature Sensor
                |
             ESP32-C3
                |
                v
           HiveMQ Broker
                |
                v
          GNS3 Gateway <--- Simulated DO Sensor
                ^       <--- Simulated pH Sensor
                |
          Attacker Node
                |
                v
        Security Verification
                |
                v
       Sensor and Security Events
                |
                v
         Node-RED Dashboard
                |
                v
       Logical NORMAL / SAFE/HOLD
```

The physical temperature readings are received from HiveMQ by the GNS3 gateway.

The dissolved oxygen and pH sensors are simulated in the virtual environment.

The security gateway applies message-verification and replay checks to supported sensor pathways.

The dashboard displays monitoring information and logical control states.

## 6. Existing Project Files

The repository already contains documentation and code for earlier development stages, including:

- `README.md`
- `docs/project-management/project-plan.md`
- `docs/project-management/implementation-status.md`
- `docs/team-roles.md`
- `scripts/sensors/`
- `scripts/monitoring/`
- `scripts/gateway/`
- `testing/`
- `docs/gns3/`

Some files belong to the earlier Python/Mosquitto prototype and should be distinguished from the final showcase implementation.

## 7. Final Documentation Still Needed

To improve reproducibility, the team should consolidate:

- Final GNS3 topology and setup configuration
- Final GNS3 gateway source code
- Simulated dissolved oxygen and pH sensor scripts
- Attacker-node demonstration scripts
- Physical ESP32 Arduino sketch
- HiveMQ integration configuration instructions
- Node-RED dashboard flow export
- Final attack demonstration logs or screenshots
- Logical SAFE/HOLD demonstration results
- Final installation and startup instructions

Credentials, passwords, private keys and secret tokens must not be uploaded.

## 8. Team Collaboration

The project requirements were addressed collaboratively by Sahil, Neha and Arnob.

Different members focused on different technical areas, but system integration, testing, troubleshooting and documentation involved shared team activities.

GitHub commits and uploads represent repository activity and should not be interpreted as proof of exclusive ownership of a feature.

## 9. Limitations and Future Work

AQ-1 is an academic cybersecurity prototype.

Future improvements may include:

- Additional physical water-quality sensors
- Stronger MQTT authentication and access-control testing
- Consistent replay protection across all sensor pathways
- Improved cryptographic key management
- More extensive availability and recovery testing
- Persistent monitoring storage and recovery procedures
- Physical actuator and pump integration
- Longer-term testing under real farm conditions

These improvements should not be presented as completed features.

## 10. Traceability Principle

Each major project requirement should connect to:

**Requirement → Implementation → Test → Observed Result → Documentation**

The team should distinguish between a feature demonstrated during the showcase and complete implementation files already available in GitHub.

This keeps project reporting accurate and allows future students or reviewers to understand the system.

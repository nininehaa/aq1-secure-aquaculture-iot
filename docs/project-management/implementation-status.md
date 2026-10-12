# AQ-1 Project Plan and Implementation Record

**Project:** AQ-1 Secure and Resilient IoT Sensor-Control System  
**Client Scenario:** Coral Coast Aquaculture  
**Course:** COIT13236 Cyber Security Project  
**Team:** Neha Thanait, Sahil Basnet and Md Monirul Haque Arnob  
**Updated:** 12 October 2026

## 1. Project Purpose

The purpose of AQ-1 is to demonstrate how cybersecurity controls can protect IoT sensor information used in aquaculture monitoring.

Aquaculture farms depend on accurate water-quality readings to maintain suitable conditions for fish and prawns. Compromised, forged, replayed or unavailable readings can lead to incorrect monitoring and operational decisions.

AQ-1 focuses on verifying incoming sensor data, detecting malicious messages and demonstrating logical supervisory responses when information cannot be trusted.

## 2. Project Objectives

The main objectives are to:

1. Develop a virtual aquaculture network using GNS3.
2. Simulate dissolved oxygen (DO) and pH sensor readings.
3. Integrate a physical ESP32-C3 temperature sensor.
4. Use MQTT to communicate sensor data.
5. Implement gateway-side HMAC-SHA256 verification.
6. Detect spoofing, tampering and replay attacks.
7. Monitor sensor availability and security events.
8. Display relevant information through a Node-RED dashboard.
9. Demonstrate logical NORMAL and SAFE/HOLD states.
10. Document implementation, testing, individual contributions and limitations.

Physical pump or aerator operation is outside the implemented scope.

## 3. Project Scope

### Implemented Showcase Components

| Component | Implementation |
|---|---|
| Dissolved oxygen | Simulated sensor in GNS3 |
| pH | Simulated sensor in GNS3 |
| Temperature | Physical DS18B20 connected to ESP32-C3 |
| ESP32 programming | Arduino IDE |
| Physical sensor communication | HiveMQ MQTT broker |
| Security gateway | Python gateway running in GNS3 |
| Security checks | HMAC, sensor identity and replay checking |
| Attack demonstrations | Spoofing, tampering and replay |
| Monitoring interface | Node-RED dashboard developed by Arnob |
| Control demonstration | Logical NORMAL and SAFE/HOLD states |

### Excluded from the Final Showcase

The project did not demonstrate:

- Physical pump or aerator actuation
- Physical dissolved oxygen or pH sensors
- Wireshark packet-capture analysis
- Azure as the final dashboard
- A production-ready automated aquaculture facility

These should not be described as completed deliverables.

## 4. System Architecture

The project integrates a physical temperature sensor with simulated sensor nodes in a GNS3 environment.

```text
Physical DS18B20 Temperature Sensor
                |
                v
             ESP32-C3
          (Arduino IDE)
                |
                v
          HiveMQ Broker
                |
                v
          GNS3 Gateway <------ Simulated DO Sensor
                ^         <--- Simulated pH Sensor
                |
         Attacker/Test Node
                |
                v
        Security Verification
        - HMAC checks
        - Sensor identity
        - Sequence checking
        - Availability monitoring
                |
                v
        Accepted / Rejected Data
          Alerts / Control State
                |
                v
         Node-RED Dashboard
                |
                v
        Logical NORMAL / SAFE/HOLD
```

The physical temperature measurements are published using MQTT and received by the GNS3 gateway through HiveMQ.

The DO and pH sensors are simulated in GNS3.

The security gateway validates incoming information before it is treated as trusted. The Node-RED dashboard presents sensor and security information.

## 5. Project Development Phases

### Phase 1 — Initial Python and MQTT Prototype

**Status: Completed as an early prototype**

The project initially used Python-based sensor simulations and Eclipse Mosquitto MQTT.

This stage introduced:

- Sensor-message publishing and subscribing
- Basic dissolved oxygen and temperature data generation
- HMAC generation and verification
- Tampered-message rejection
- Monitoring and outage detection
- Security event logging

This work established the technical foundation for later development.

### Phase 2 — GNS3 Network Development

**Status: Demonstrated**

The team expanded the project into GNS3 following lecturer feedback about the need for a more substantial technical implementation.

Activities included:

- Building and configuring virtual network components
- Configuring virtual machines and connectivity
- Creating simulated sensor nodes
- Integrating the security gateway
- Troubleshooting network connectivity
- Testing communication between project components

The GNS3 environment allowed the team to demonstrate IoT security in a networked environment rather than relying only on local Python scripts.

### Phase 3 — Physical Temperature Sensor Integration

**Status: Demonstrated**

Neha and Sahil worked together on integrating a physical DS18B20 temperature sensor with an ESP32-C3 microcontroller.

Arduino IDE was used to develop and upload the microcontroller program.

The ESP32-C3 transmitted temperature readings through HiveMQ.

The GNS3 gateway successfully received these physical measurements.

### Phase 4 — Cybersecurity Attack Testing

**Status: Demonstrated**

The GNS3 environment was used to test three controlled attacks.

| Attack | Test objective | Expected result |
|---|---|---|
| Spoofing | Send a forged message claiming a legitimate sensor identity | Gateway rejects invalid authentication or integrity |
| Tampering | Modify a message after HMAC generation | Gateway rejects the mismatched HMAC |
| Replay | Resend an earlier valid message | Gateway rejects the repeated sequence number |

The purpose of these tests was to demonstrate how different security controls respond to different attack methods.

### Phase 5 — Node-RED Dashboard and Logical Control

**Status: Demonstrated**

Arnob developed the Node-RED dashboard used in the final project showcase.

The dashboard presents relevant sensor information, security events and logical control states.

The software demonstrates NORMAL and SAFE/HOLD status behaviour.

No physical pump or relay was operated.

### Phase 6 — Final Documentation and Evidence

**Status: In progress**

The team is aligning the GitHub repository with the final implementation and consolidating evidence.

Remaining documentation tasks include:

- Saving the final GNS3 project and setup instructions
- Adding final gateway and sensor scripts
- Including attacker-node scripts
- Documenting physical ESP32 integration
- Exporting the Node-RED flow
- Recording attack demonstration results
- Updating architecture documentation
- Correcting outdated project-status information
- Updating individual contribution evidence

## 6. Team Responsibilities

### Sahil Basnet — Sensor and Network Communication

Main areas of work:

- MQTT communication and sensor publishing
- Network configuration and troubleshooting
- GNS3 integration
- Physical ESP32-C3 temperature-sensor development with Neha
- Sensor-message generation and related security testing

### Neha Thanait — Security Monitoring and Trust Validation

Main areas of work:

- HMAC verification and sensor-message validation
- Sensor outage and recovery monitoring
- Security event logging and alerts
- Testing and evidence preparation
- GNS3 integration and troubleshooting
- Physical ESP32-C3 temperature-sensor development with Sahil
- Technical documentation

### Md Monirul Haque Arnob — Dashboard and Control Integration

Main areas of work:

- Node-RED dashboard development
- GNS3 integration
- Security and sensor-status visualisation
- Logical control-state integration
- NORMAL and SAFE/HOLD behaviour

All members contributed to integrating their individual components into the overall demonstration.

## 7. Testing and Acceptance Criteria

| ID | Acceptance criterion | Reported status |
|---|---|---|
| AC-01 | Simulated DO readings received by gateway | Demonstrated |
| AC-02 | Simulated pH readings received by gateway | Demonstrated |
| AC-03 | Physical ESP32 temperature readings received through HiveMQ | Demonstrated |
| AC-04 | Valid HMAC-protected messages accepted | Demonstrated |
| AC-05 | Spoofing messages rejected | Demonstrated |
| AC-06 | Tampered messages rejected | Demonstrated |
| AC-07 | Replayed messages rejected | Demonstrated |
| AC-08 | Sensor availability monitored | Implemented in earlier prototype; final evidence to be consolidated |
| AC-09 | Sensor and security information displayed in Node-RED | Demonstrated |
| AC-10 | Logical NORMAL and SAFE/HOLD states shown | Demonstrated |
| AC-11 | Physical pump operation | Outside scope |
| AC-12 | Final source code, setup and testing evidence in GitHub | In progress |

A demonstrated feature refers to behaviour observed during project testing or the showcase. It does not necessarily mean that its final source files and evidence are already uploaded to GitHub.

## 8. Tools and Technologies

The project used:

- Python
- GNS3
- ESP32-C3
- DS18B20 temperature sensor
- Arduino IDE
- HiveMQ MQTT broker
- Eclipse Mosquitto MQTT for the initial prototype
- HMAC-SHA256
- Node-RED
- Git and GitHub

SQLite was also used in the team's monitoring/data-handling work.

## 9. Project Risks and Challenges

### Network Configuration

GNS3 virtual machines, adapters and connectivity required repeated troubleshooting.

**Learning:** Working network configurations should be recorded and verified before further integration.

### Hardware Integration

The ESP32-C3 required configuration, programming and testing before it could transmit physical temperature data.

**Learning:** Hardware components should be tested independently before integrating them with the gateway.

### Security Integration

Sensor messages and gateway verification needed compatible sensor identities, message formats and HMAC calculations.

**Learning:** Shared message formats and configuration details should be agreed upon early.

### Team Integration

Different members developed components that depended on one another.

**Learning:** Regular integration testing and consistent documentation are necessary to reduce last-minute compatibility problems.

## 10. Limitations and Future Improvements

AQ-1 is an academic prototype intended to demonstrate cybersecurity concepts and practical IoT integration.

Potential future improvements include:

- Physical dissolved oxygen and pH sensors
- Physical pump or aerator control
- Stronger key management
- TLS protection where not currently configured
- More comprehensive MQTT access-control testing
- Replay protection across all sensor pathways
- Persistent and reliable monitoring storage
- Long-term sensor outage and recovery testing
- Improved deployment and recovery procedures
- Testing under actual aquaculture conditions

These are future improvements rather than completed showcase features.

## 11. Documentation and Evidence

The repository contains earlier prototype code, test plans and project documentation.

The final implementation should be recorded using:

- Source code and configuration
- GNS3 topology and node setup
- ESP32 Arduino sketch
- Node-RED dashboard/flow export
- Security attack test results
- Screenshots and logs
- Team contribution records

The required evidence chain is:

`Requirement → Implementation → Execution → Test Result → Evidence`

## 12. Project Outcome

AQ-1 demonstrates how a simulated aquaculture network can be combined with a real IoT temperature sensor and cybersecurity verification.

Through HMAC verification, attack detection, sensor monitoring and Node-RED visualisation, the project shows why aquaculture sensor readings must be verified before being trusted.

The main contribution is the integration of IoT monitoring, cybersecurity detection and logical safe-control behaviour within an academic prototype.

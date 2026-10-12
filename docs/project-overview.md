# AQ-1 Project Overview

## Project Title

AQ-1 Secure and Resilient IoT Sensor-Control System

## Client

Coral Coast Aquaculture

## Team Members

- Sahil Basnet
- Neha Thanait
- Md Monirul Haque Arnob

## Project Scenario

AQ-1 — IoT/Sensor Security for a Prawn and Barramundi Farm

## 1. Business Problem

Aquaculture farms depend on reliable water-quality information to maintain suitable living conditions for fish and prawns.

Important measurements include dissolved oxygen (DO), pH and temperature. These parameters can affect aquatic health, farm productivity and operational decisions.

IoT sensors provide automated monitoring, but they also introduce cybersecurity risks.

An attacker may impersonate a legitimate sensor, modify transmitted readings or replay previously valid data. If the monitoring system accepts unreliable information, operators may make decisions based on incorrect water conditions.

Sensor communication failures can also prevent important information from reaching the monitoring system.

AQ-1 addresses these risks by demonstrating cybersecurity verification and monitoring techniques in an aquaculture scenario.

## 2. Project Aim

The aim of AQ-1 is to develop an integrated IoT cybersecurity demonstration that verifies sensor information before it is trusted.

The system combines simulated water-quality sensors, a physical temperature sensor, MQTT communication, security verification and dashboard monitoring.

The main objectives are to:

- Verify sensor-message integrity and authenticity using HMAC-SHA256.
- Detect spoofing, tampering and replay attacks.
- Monitor sensor availability.
- Integrate physical IoT measurements with the GNS3 network environment.
- Display sensor information and security events through Node-RED.
- Demonstrate logical NORMAL and SAFE/HOLD responses when information cannot be trusted.

## 3. Sensor Implementation

The project uses three water-quality measurements.

| Measurement | Implementation |
|---|---|
| Dissolved oxygen (DO) | Simulated in GNS3 |
| pH | Simulated in GNS3 |
| Temperature | Physical DS18B20 sensor connected to ESP32-C3 |

The simulated DO and pH sensors generate readings within the virtual aquaculture environment.

The physical temperature sensor measures actual temperature and publishes data through HiveMQ.

The gateway running in GNS3 receives the physical temperature readings and processes the messages.

This demonstrates integration between physical IoT hardware and a virtualised cybersecurity environment.

## 4. System Architecture

```text
Physical DS18B20 Temperature Sensor
                |
             ESP32-C3
                |
                v
          HiveMQ Broker
                |
                v
          GNS3 Gateway <---- Simulated DO Sensor
                ^        <---- Simulated pH Sensor
                |
          Attacker Node
                |
                v
         Security Verification
         - HMAC validation
         - Sensor identity
         - Replay detection
         - Availability monitoring
                |
                v
       Sensor Data / Security Events
                |
                v
          Node-RED Dashboard
                |
                v
        Logical NORMAL / SAFE/HOLD
```

The GNS3 gateway processes incoming sensor messages and applies security checks.

The attacker node supports controlled cybersecurity demonstrations.

The Node-RED dashboard presents monitoring information and logical control status.

## 5. Cybersecurity Features

### HMAC-SHA256 Message Verification

Sensor messages are checked using an agreed cryptographic key and message format.

The gateway calculates the expected HMAC and compares it with the received value.

Messages with invalid HMAC values are rejected.

### Spoofing Detection

A simulated attacker attempts to impersonate a legitimate sensor and submit forged data.

The gateway detects invalid authentication or integrity information and rejects the message.

### Tampering Detection

A sensor reading is modified without generating a matching HMAC.

The gateway identifies the mismatch and rejects the modified reading.

### Replay Detection

A previously valid sensor message is transmitted again.

The GNS3 gateway uses sequence-number checking to detect and reject repeated messages in the tested pathway.

### Sensor Availability

The monitoring components detect interruptions in valid sensor readings and support outage and recovery reporting.

### Logical SAFE/HOLD

The system demonstrates logical NORMAL and SAFE/HOLD states to indicate whether normal supervisory operation can continue.

No physical pump, aerator or relay was operated.

## 6. Node-RED Dashboard

The final project uses the Node-RED dashboard developed by Arnob.

The dashboard provides visual monitoring of sensor readings, system information and security-related events.

Its purpose is to help users observe sensor activity and identify situations requiring attention.

Node-RED is the final showcase dashboard, rather than the older Azure dashboard implementation contained in the repository.

## 7. Project Development

### Initial Prototype

The project initially used Python sensor simulations and Eclipse Mosquitto MQTT.

The prototype established basic sensor communication, HMAC verification, monitoring and security tests.

### GNS3 Development

The team expanded the project into GNS3 to simulate networked sensors, configure a gateway and test cybersecurity attacks.

The virtual environment supported simulated dissolved oxygen and pH readings.

### Physical IoT Integration

A physical DS18B20 temperature sensor was integrated with ESP32-C3 using Arduino IDE.

The device published temperature readings through HiveMQ, which were successfully received by the GNS3 gateway.

### Final Monitoring and Security Demonstration

The team integrated the security gateway, attack-testing environment and Node-RED dashboard to demonstrate monitoring and cybersecurity responses.

## 8. Technologies Used

- Python
- GNS3
- ESP32-C3
- DS18B20 temperature sensor
- Arduino IDE
- HiveMQ MQTT broker
- Eclipse Mosquitto MQTT for the initial prototype
- HMAC-SHA256
- Node-RED
- GitHub

## 9. Project Limitations

AQ-1 is an academic cybersecurity prototype rather than a production-ready aquaculture control system.

The project did not include:

- Physical dissolved oxygen or pH sensors.
- Physical pump or aerator operation.
- A fully automated physical farm-control system.
- Wireshark packet-capture analysis as part of the final demonstration.

Potential future improvements include stronger key management, additional physical sensors, extended security testing, more comprehensive replay protection and physical actuator integration.

## 10. Project Outcome

AQ-1 demonstrates how cybersecurity techniques can help protect aquaculture monitoring systems against unreliable or malicious sensor information.

By combining physical temperature sensing, simulated dissolved oxygen and pH measurements, MQTT communication, GNS3 gateway security and Node-RED monitoring, the team created an integrated demonstration of secure IoT data handling.

The project highlights the importance of verifying sensor messages, identifying cyberattacks and displaying appropriate logical control states when trusted information becomes unavailable.

## 11. Team Collaboration

The project was developed collaboratively by Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob.

All members contributed through technical development, configuration, testing, troubleshooting, integration and documentation, with different areas of focus throughout the project.

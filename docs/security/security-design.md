# AQ-1 Cybersecurity Design

**Project:** AQ-1 Secure and Resilient IoT Sensor-Control System  
**Client:** Coral Coast Aquaculture  
**Course:** COIT13236 Cyber Security Project  
**Team:** Sahil Basnet, Neha Thanait and Md Monirul Haque Arnob

## 1. Security Design Overview

AQ-1 demonstrates how cybersecurity controls can protect sensor information used in aquaculture monitoring.

In a real aquaculture environment, incorrect sensor readings could influence operational decisions and potentially affect aquatic livestock.

The main concern is not only whether sensors can communicate, but whether the information received can be trusted.

The project combines simulated dissolved oxygen and pH sensors, a physical temperature sensor, a GNS3 security gateway and a Node-RED monitoring dashboard.

The security design focuses on message integrity, source authentication, replay protection, sensor availability and logical safe-control responses.

## 2. Security Objectives

| Objective | Description | Project approach |
|---|---|---|
| Integrity | Detect unauthorised modification of sensor messages | HMAC-SHA256 |
| Authenticity | Verify messages against expected sensor identities and shared keys | Sensor identity and HMAC verification |
| Availability | Identify interruptions in valid sensor data | Timeout-based monitoring |
| Replay protection | Prevent previously processed messages from being accepted as new | Sequence-number checking |
| Monitoring | Make suspicious or unavailable data visible | Gateway alerts and Node-RED dashboard |
| Safe response | Indicate when unreliable information should not support normal control decisions | Logical SAFE/HOLD state |

## 3. Security Architecture

```text
SIMULATED SENSOR NETWORK                PHYSICAL SENSOR
          |                                   |
     DO and pH                           DS18B20
          |                                   |
          |                                ESP32-C3
          |                                   |
          |                                HiveMQ
          |                                   |
          +----------------+------------------+
                           |
                           v
                   GNS3 Security Gateway
                           |
                   Message Validation
                   - Sensor identity
                   - HMAC verification
                   - Replay protection
                   - Availability checks
                           |
               +-----------+-----------+
               |           |           |
             VALID       INVALID      OUTAGE
               |           |           |
             ACCEPT       REJECT      ALERT
               |           |           |
               +-----------+-----------+
                           |
                           v
                    Node-RED Dashboard
                           |
                           v
                  NORMAL / SAFE-HOLD
```

The GNS3 security gateway is responsible for evaluating incoming messages.

The Node-RED dashboard presents relevant sensor and security-monitoring information.

## 4. HMAC-SHA256 Message Integrity

HMAC-SHA256 is used to check whether protected sensor-message contents have been modified.

The sender creates an HMAC using an agreed secret key and the message fields.

The gateway independently calculates the expected HMAC and compares the two values.

A message is rejected if the HMAC comparison fails.

### Example

A legitimate dissolved oxygen sensor reports:

`DO-001: 6.5 mg/L`

An attacker modifies the value to:

`DO-001: 1.0 mg/L`

If the attacker cannot generate the correct HMAC, the gateway detects the mismatch and rejects the modified reading.

HMAC provides integrity and message authentication, but it does not provide encryption.

## 5. Sensor Identity Verification

Each sensor message includes an identity that allows the gateway to determine which sensor it claims to represent.

The gateway checks the identity against the expected sensor configuration and verifies the corresponding message-integrity information.

An identity field alone is insufficient proof of authenticity because an attacker can copy or forge it.

For this reason, sensor identity checks are combined with cryptographic verification.

## 6. Replay Attack Protection

A replay attack occurs when an attacker retransmits a previously legitimate sensor message.

The old message can contain a valid HMAC because it has not been modified.

The tested GNS3 gateway uses sequence-number checking to identify messages that have already been processed.

When a message arrives with a sequence number that is not newer than the last accepted sequence number for that sensor, the gateway can reject it.

Timestamp freshness checks may also be applied to supported message formats.

The physical ESP32-C3 pathway should be assessed separately where its timestamp representation or sequence handling differs from the simulated GNS3 sensors.

## 7. Sensor Availability Monitoring

Sensor availability is an important part of IoT security.

A sensor may stop publishing because of a communication failure, device problem or deliberate interference.

The project includes timeout-based monitoring developed during the initial prototype.

The monitoring logic tracks the last accepted reading from expected sensors.

If a sensor stops producing valid readings beyond its configured timeout, an outage warning can be generated.

Invalid sensor messages should not be counted as valid readings simply to prevent an outage alert.

## 8. Controlled Cybersecurity Attacks

AQ-1 demonstrates three attack scenarios using the GNS3 environment.

### Attack 1 — Spoofing

**Objective:** Impersonate a legitimate sensor.

**Method:** The attacker node submits a forged sensor reading claiming a trusted sensor identity.

**Expected response:** The gateway detects invalid authentication or HMAC information and rejects the forged message.

### Attack 2 — Tampering

**Objective:** Change a sensor reading without authorisation.

**Method:** The attacker modifies the value in a previously prepared message while retaining the original HMAC.

**Expected response:** The gateway recalculates the HMAC, detects a mismatch and rejects the message.

### Attack 3 — Replay

**Objective:** Reuse a previously valid sensor message.

**Method:** The attacker retransmits a message containing an earlier accepted sequence number.

**Expected response:** The gateway detects the repeated sequence number and rejects the replayed message.

These scenarios are important because they test different weaknesses.

HMAC helps prevent message tampering, while sequence-number checking helps prevent replay of otherwise valid messages.

## 9. Node-RED Security Monitoring

The final system uses Arnob's Node-RED dashboard.

The dashboard provides a visual interface for observing sensor data and relevant security information.

It can present:

- Sensor readings.
- Sensor availability.
- Security alerts.
- Accepted and rejected message information.
- Logical control status.

The dashboard is responsible for presenting monitoring information rather than independently performing all cryptographic verification.

The gateway remains the main security-verification component.

## 10. Logical SAFE/HOLD Control

The project demonstrates two supervisory states.

### NORMAL

The system has acceptable trusted sensor information for monitoring.

### SAFE/HOLD

The system identifies a condition involving untrusted or unavailable sensor information that requires a safety-oriented response.

This represents logical software-control behaviour.

**The project did not implement a working physical pump, aerator or relay.**

The control state therefore indicates a software decision rather than actual operation of physical farm equipment.

## 11. MQTT Communication and Security

MQTT is used for sensor communication.

### HiveMQ

The physical ESP32-C3 temperature sensor publishes readings through HiveMQ, which are received by the GNS3 gateway.

### Eclipse Mosquitto

Mosquitto was used during the earlier Python-based prototype.

### Security Considerations

MQTT communication requires protection against unauthorised clients and message interception.

Relevant security improvements include:

- Broker authentication.
- Topic-based access control.
- TLS encryption.
- Secure management of credentials and HMAC keys.
- Monitoring of unexpected publishing behaviour.

HMAC does not provide confidentiality, so it should not be treated as a substitute for transport encryption.

The presence of a security feature in the design does not automatically mean that it was configured and tested in every deployment pathway.

## 12. Limitations

The project is an academic cybersecurity prototype rather than a production-ready industrial monitoring solution.

The following limitations remain:

- DO and pH sensors were simulated rather than physical hardware.
- Physical pump and aerator control was not implemented.
- Security controls may differ between the GNS3 simulated sensor paths and the physical ESP32 pathway.
- Stronger MQTT access control and key management require further hardening and validation.
- Comprehensive production resilience and long-term reliability testing were outside the showcase scope.

## 13. Future Security Improvements

Future work could include:

- Consistent replay protection across all sensor pathways.
- MQTT connections protected with TLS where not already configured.
- More comprehensive broker permissions and topic access controls.
- Stronger device identity and key-management procedures.
- Longer-term sensor outage and recovery testing.
- Security-event persistence and audit logging.
- Network segmentation and firewall validation.
- Additional physical sensors and actuator integration.

These improvements are not claimed as completed functionality.

## 14. Security Design Outcome

AQ-1 demonstrates the importance of verifying sensor information before treating it as trustworthy.

The project uses cryptographic message verification, replay detection, monitoring and controlled cybersecurity attacks to show how unreliable data can be identified.

By integrating these controls with GNS3, physical temperature sensing and Node-RED monitoring, the system provides a practical demonstration of cybersecurity principles relevant to aquaculture IoT environments.

# AQ-1 Implementation Status

**Project:** AQ-1 Secure and Resilient Aquaculture IoT Sensor-Control System  
**Client:** Coral Coast Aquaculture  
**Status reviewed:** 12 October 2026

## 1. Purpose

This document records the final AQ-1 implementation and distinguishes between the initial prototype, demonstrated functionality and future improvements.

The final showcase combines two simulated water-quality sensors, one physical temperature sensor, a GNS3 network, cybersecurity verification, controlled attack demonstrations and a Node-RED monitoring dashboard.

## 2. Implementation Summary

| Component | Implementation status | Details |
|---|---|---|
| Dissolved oxygen (DO) | Demonstrated | Simulated sensor running in GNS3 |
| pH | Demonstrated | Simulated sensor running in GNS3 |
| Physical temperature | Demonstrated | DS18B20 connected to ESP32-C3 |
| ESP32-C3 programming | Implemented | Arduino IDE |
| Physical MQTT communication | Demonstrated | ESP32 publishes through HiveMQ |
| GNS3 gateway integration | Demonstrated | Gateway successfully receives physical temperature readings from HiveMQ |
| HMAC-SHA256 verification | Demonstrated | Gateway validates message integrity |
| Spoofing detection | Demonstrated | Forged sensor messages rejected |
| Tampering detection | Demonstrated | Modified sensor messages rejected |
| Replay detection | Demonstrated | Previously processed sequence numbers rejected |
| Sensor outage monitoring | Implemented in earlier prototype | Final multi-sensor test evidence to be consolidated |
| Node-RED dashboard | Demonstrated | Dashboard developed by Arnob |
| Logical NORMAL / SAFE-HOLD | Demonstrated | Software-based supervisory control states |
| Physical pump or relay | Not implemented | No physical actuation was demonstrated |
| Azure dashboard | Not part of final showcase | Older repository implementation only |
| Wireshark | Not used | No packet-capture claim |

The final GNS3 gateway and Node-RED files still need to be consolidated in the GitHub repository, together with screenshots and final demonstration results.

## 3. Final System Architecture

```text
Physical DS18B20
      |
   ESP32-C3
      |
    HiveMQ
      |
      v
 GNS3 Gateway <--- Simulated DO Sensor
      ^        <--- Simulated pH Sensor
      |
 GNS3 Attacker Node
      |
      v
 Security Verification
      |
      +-- Accepted readings
      +-- Rejected readings
      +-- Security alerts
      |
      v
 Node-RED Dashboard
      |
      v
 Logical NORMAL / SAFE-HOLD Status
```

The physical temperature sensor sends real measurements through HiveMQ. The security gateway running in GNS3 receives the MQTT data.

The simulated DO and pH sensors provide additional measurements within the virtual environment.

The attacker node provides controlled malicious messages for testing the gateway's cybersecurity controls.

## 4. Security Implementation

### HMAC Verification

The gateway checks received HMAC values against the expected values calculated using the agreed keys and message formats.

Messages that fail validation are rejected.

### Spoofing Attack

The attacker attempts to impersonate a legitimate sensor by submitting a forged message.

The gateway identifies failed verification and rejects the message.

### Tampering Attack

The attacker modifies a sensor reading without generating a matching valid HMAC.

The gateway detects the mismatch and rejects the altered data.

### Replay Attack

The attacker resends a previously valid sensor message.

The gateway uses sequence-number checks to identify and reject repeated messages in the tested GNS3 pathway.

Replay protection across all sensor pathways, including the physical ESP32, should be recorded separately where implementation differs.

### Availability Monitoring

The earlier monitoring prototype includes timeout-based outage and recovery detection.

Any final GNS3 outage-test results should be recorded with the corresponding gateway logs or screenshots.

## 5. Dashboard and Control

The final showcase used Arnob's Node-RED dashboard to present sensor readings, monitoring information and security-related states.

The demonstration included logical NORMAL and SAFE/HOLD status information.

**The team did not implement physical pump or aerator control.** The control component demonstrates software states, not operation of real farm equipment.

## 6. Initial Prototype vs Final Showcase

| Initial prototype | Final showcase |
|---|---|
| Python-based sensor producers | Simulated DO and pH sensors in GNS3 |
| Python temperature simulation | Physical ESP32-C3 temperature sensor |
| Local Mosquitto communication | HiveMQ for physical temperature messages |
| Initial HMAC and outage testing | GNS3 gateway and attack demonstrations |
| Local console-based monitoring |  Node-RED dashboard |
| SAFE/HOLD design and planning | Logical software control-state demonstration |

The initial prototype remains valuable evidence of the project's technical development.

## 7. Evidence Already in GitHub

The existing repository contains earlier development evidence, including:

- `scripts/sensors/`
- `scripts/monitoring/`
- `scripts/gateway/gateway.py` — earlier prototype gateway
- `testing/Week_6_Security_Test_Plan.md`
- `testing/security-test-results.md`
- `docs/evidence/`
- `docs/gns3/`

These files should not automatically be treated as the complete final showcase implementation.

## 8. Evidence Still to Consolidate

The following artefacts should be added or linked where available:

- Final GNS3 project/topology
- Final gateway Python script and configuration
- Simulated DO and pH sensor scripts used in the showcase
- Attacker-node demonstration scripts
- Screenshots or logs from spoofing, tampering and replay tests
- ESP32 Arduino sketch or firmware source
- Physical temperature-to-HiveMQ-to-GNS3 test evidence
- Arnob's Node-RED flow export and dashboard screenshots
- Logical SAFE/HOLD demonstration evidence
- Final configuration and setup instructions

Do not upload private credentials, HiveMQ passwords, HMAC secrets or tokens.

## 9. Limitations

AQ-1 is an academic cybersecurity demonstration, not a production-ready automated aquaculture facility.

The project did not include physical DO or pH sensors, a working physical pump, or physical aerator automation.

Additional security hardening, long-term testing, key management, network reliability testing and integration with real farm equipment remain possible future improvements.

## 10. Completion Criteria

A component should be treated as fully evidenced when the team can identify:

1. Its implementation or configuration.
2. How it was executed.
3. The observed result.
4. The related source code or artefact.
5. The screenshot, log or test result supporting the claim.

The final demonstration and the GitHub documentation should remain consistent.

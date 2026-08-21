# Security Test Results

## Purpose

This document gives a simple consolidated view of the security and resilience tests completed so far for the AQ-1 Coral Coast Aquaculture prototype.

Detailed test steps remain in `testing/Week_6_Security_Test_Plan.md`. This file is the quick evidence summary.

## Current Test Environment

The current prototype uses:

- Python dissolved-oxygen sensor simulator
- Python temperature sensor simulator
- Eclipse Mosquitto MQTT broker
- Python monitoring component
- HMAC-SHA256 message integrity
- local MQTT communication on port `1883`

## Results Summary

| Test ID | Test | Result | Meaning |
|---|---|---|---|
| TC-W6-01 | Valid DO HMAC | PASS | Legitimate DO reading accepted |
| TC-W6-02 | Invalid DO HMAC | PASS | Modified DO reading rejected |
| TC-W6-03 | Malformed DO message | PASS | Invalid message not trusted |
| TC-W6-04 | DO sensor outage | PASS | Missing DO data detected |
| TC-W6-05 | DO sensor recovery | PASS | Recovery recorded when valid readings resume |
| TC-W6-06 | Temperature outage | PASS | Temperature outage detected independently |
| TC-W6-07 | Temperature recovery | PASS | Temperature recovery detected |
| TC-W6-08 | Missing MQTT credentials | PASS | Unauthenticated MQTT client rejected |
| TC-W6-09 | SAFE/HOLD activation | PENDING | Control integration not yet completed |
| TC-W6-10 | Valid temperature HMAC | PASS | Legitimate signed temperature reading accepted |
| TC-W6-11 | Tampered temperature message | PASS | Altered temperature reading rejected by HMAC verification |

## MQTT Authentication Test

### Goal

Confirm that anonymous or unauthenticated clients cannot access the secured Mosquitto broker.

### Valid Client

An MQTT subscriber using the configured `TEMP-001` credentials successfully connected and received live temperature messages.

### Invalid Client

A subscriber was started without supplying a username or password.

Observed result:

```text
Connection Refused: not authorised
```

### Result

PASS.

This proves that the broker-side authentication control is active for the tested configuration.

## Temperature Integrity Test

### Goal

Confirm that a temperature message cannot be modified after signing without detection.

### Method

The controlled tamper script:

1. creates an original temperature reading
2. calculates its HMAC-SHA256 value
3. changes the temperature value and status after signing
4. keeps the original HMAC
5. publishes the altered message

### Result

The monitor recalculated the expected HMAC, detected a mismatch and rejected the message.

PASS.

## Sensor Outage and Recovery Testing

The monitoring system tracks expected sensors independently.

When a sensor stops sending valid readings for longer than the configured timeout, the monitor raises an outage alert. When valid readings resume, a recovery event is recorded.

This behaviour has been tested for both dissolved oxygen and temperature sensors.

## What the Current Tests Prove

The current prototype demonstrates that:

- sensor messages can be integrity protected with HMAC-SHA256
- altered HMAC-protected messages can be rejected
- malformed sensor data is not treated as trusted
- sensor outages can be detected
- sensor recovery can be recorded
- Mosquitto can reject a client that does not provide valid authentication information

## What Is Not Yet Proven

The current tests do not yet prove the complete final architecture.

Still pending or incomplete:

- `SAFE/HOLD` control activation
- fully authenticated monitoring-client connection to the secured broker
- topic-level MQTT ACL enforcement
- TLS-protected MQTT transport
- GNS3 network segmentation
- firewall-rule testing
- packet-capture evidence across the virtual network
- primary/backup broker resilience

## Evidence Locations

- `testing/Week_6_Security_Test_Plan.md`
- `scripts/sensors/do_sensor.py`
- `scripts/sensors/temperature_sensor.py`
- `scripts/security/temperature_tamper_test.py`
- `scripts/monitoring/monitor.py`
- `configs/mosquitto/mosquitto.conf`
- `docs/progress/week-6.md`
- `docs/progress/sahil-week6-progress.md`

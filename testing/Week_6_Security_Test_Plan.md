# Week 6 Security Test Plan

## Project
Secure and Resilient IoT Sensor-Control System for Coral Coast Aquaculture

## Purpose
This test plan records Week 6 security and resilience testing for the AQ-1 prototype.

The tests focus on:
- message integrity
- sensor outage detection
- recovery detection
- malformed or tampered message rejection
- MQTT authentication
- pending fail-safe testing

## Test Environment

- Python sensor simulators
- Eclipse Mosquitto MQTT broker
- Python monitoring component
- Dissolved oxygen sensor
- Temperature sensor
- MQTT topics:
  - `aquaculture/sensors/dissolved_oxygen`
  - `aq1/pond1/temperature`

---

## TC-W6-01 — Valid DO HMAC

**Objective:** Verify that a legitimate dissolved oxygen message with a valid HMAC is accepted.

**Expected Result:**  
The monitor accepts the message and displays `HMAC: VALID`.

**Actual Result:**  
Valid dissolved oxygen messages were accepted.

**Status:** PASS

---

## TC-W6-02 — Invalid DO HMAC

**Objective:** Verify that a modified or spoofed dissolved oxygen message with an invalid HMAC is rejected.

**Expected Result:**  
The monitor rejects the message and reports `HMAC verification failed`.

**Actual Result:**  
The tampered message was rejected with a security alert.

**Status:** PASS

---

## TC-W6-03 — Malformed DO Message

**Objective:** Verify that malformed or non-JSON sensor messages are not treated as trusted readings.

**Expected Result:**  
The monitor rejects the malformed message.

**Actual Result:**  
Malformed test messages were rejected.

**Status:** PASS

---

## TC-W6-04 — DO Sensor Outage

**Objective:** Verify that the monitoring component detects loss of dissolved oxygen sensor readings.

**Expected Result:**  
An outage alert is generated after more than 10 seconds without a valid DO reading.

**Actual Result:**  
The monitor generated an independent dissolved oxygen outage alert after the configured timeout.

**Status:** PASS

---

## TC-W6-05 — DO Sensor Recovery

**Objective:** Verify that the monitoring system detects when the DO sensor resumes transmission.

**Expected Result:**  
A recovery event is recorded when valid DO readings resume.

**Actual Result:**  
The monitor generated a recovery message after the DO sensor was restarted.

**Status:** PASS

---

## TC-W6-06 — Temperature Sensor Outage

**Objective:** Verify that the temperature sensor is monitored independently from the DO sensor.

**Expected Result:**  
The temperature sensor can enter an outage state without being hidden by active DO messages.

**Actual Result:**  
The monitor detected the temperature outage independently.

**Status:** PASS

---

## TC-W6-07 — Temperature Sensor Recovery

**Objective:** Verify recovery detection for the temperature sensor.

**Expected Result:**  
A recovery event is logged when temperature readings resume.

**Actual Result:**  
The monitor generated a temperature recovery event after the sensor restarted.

**Status:** PASS

---

## TC-W6-08 — Invalid MQTT Credentials

**Objective:** Verify that unauthorised clients cannot connect to the MQTT broker.

**Expected Result:**  
A connection using missing or incorrect credentials is rejected.

**Actual Result:**  
Sahil tested the secured Mosquitto broker using an MQTT subscriber without supplying a username or password. The broker rejected the connection with `Connection Refused: not authorised`. A subscriber using the configured `TEMP-001` credentials was able to connect and receive live temperature messages.

**Status:** PASS

**Owner:** Sahil

---

## TC-W6-09 — Fail-Safe Activation

**Objective:** Verify that loss of trusted sensor data causes the control system to enter a safe state.

**Expected Result:**  
The controller enters `SAFE/HOLD` when required trusted sensor data is unavailable or invalid.

**Actual Result:**  
Not yet implemented/tested.

**Status:** PENDING

**Owner:** Arnob

---

## TC-W6-10 — Valid Temperature HMAC

**Objective:** Verify that a legitimate temperature sensor message with a valid HMAC-SHA256 signature is accepted.

**Expected Result:**  
The monitor accepts the temperature reading and displays `HMAC: VALID`.

**Actual Result:**  
The updated secure temperature sensor published signed readings and the monitor accepted them with `HMAC: VALID`.

**Status:** PASS

---

## TC-W6-11 — Tampered Temperature Message

**Objective:** Verify that a temperature message modified after signing is rejected.

**Expected Result:**  
The monitor rejects the tampered temperature message because the received HMAC no longer matches the message contents.

**Actual Result:**  
The tamper test changed the signed temperature value and status after the HMAC was generated. The monitor rejected the message and reported `HMAC verification failed`.

**Status:** PASS

---

## Week 6 Summary

The Week 6 prototype successfully demonstrates:

- HMAC-SHA256 integrity verification for dissolved oxygen readings
- rejection of tampered DO messages
- rejection of malformed DO messages
- HMAC-SHA256 integrity verification for temperature readings
- rejection of tampered temperature messages
- independent outage detection for DO and temperature
- recovery detection for both monitored sensors
- invalid or unsigned temperature data is not treated as trusted sensor activity
- broker rejection of MQTT connections without valid credentials
- authorised MQTT subscription using the configured temperature-sensor credentials

The remaining integration tasks are:

- add MQTT credentials to the monitoring client so it can operate against the authenticated broker configuration
- implement and test `SAFE/HOLD` fail-safe control
- standardise sensor MQTT topic naming and add topic-level ACLs
- continue the GNS3 virtualised deployment

## Integration Note

TC-W6-08 verifies the broker-side authentication control itself. The current monitoring script still needs its own MQTT credentials before the complete authenticated producer-to-monitor path can be demonstrated under one secure broker configuration.

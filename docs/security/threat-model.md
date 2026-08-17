# AQ-1 Threat Model

## Project

Secure and Resilient IoT Sensor-Control System for Coral Coast Aquaculture

## Purpose

This threat model identifies security threats affecting the aquaculture IoT prototype and maps each threat to a security control and a planned or completed test.

The project focuses on protecting:

- sensor identity
- message integrity
- service availability
- safe control behaviour

These areas directly support the AQ-1 scenario requirements for device authentication, integrity-protected readings, monitoring, spoof rejection, outage detection and fail-safe behaviour.

---

## System Components

The current prototype includes:

- dissolved oxygen sensor simulator
- temperature sensor simulator
- Mosquitto MQTT broker
- Python monitoring and security verification component
- planned fail-safe controller
- planned Node-RED monitoring/dashboard layer
- planned GNS3 virtualised deployment

---

## Threat 1 — Sensor Spoofing

### Description

An attacker may attempt to connect to the MQTT broker while pretending to be an authorised sensor.

A spoofed sensor could publish false readings that may influence monitoring or automated control decisions.

### Security Impact

- loss of sensor identity assurance
- false operational data
- possible unsafe control action

### Control

- MQTT username/password authentication
- broker configuration to reject anonymous or unauthorised connections
- future topic access-control rules

### Test

Attempt to connect using:

- no credentials
- incorrect credentials

### Expected Result

The MQTT broker rejects the unauthorised connection.

### Current Status

PENDING

### Owner

Sahil

---

## Threat 2 — Sensor Message Tampering

### Description

An attacker may modify a legitimate sensor reading while it is being transmitted or submit a modified reading using a copied sensor identity.

For example, a dissolved oxygen value could be changed from a safe reading to a dangerous or misleading value.

### Security Impact

- loss of message integrity
- false monitoring information
- unsafe automated decisions

### Control

HMAC-SHA256 is used to verify the integrity of dissolved oxygen sensor readings.

The sensor creates an HMAC signature from the message contents.

The monitoring component independently calculates the expected HMAC and compares it with the received signature.

### Test

Send:

1. a legitimate DO reading with a valid HMAC
2. a modified DO reading with an invalid HMAC

### Expected Result

- valid HMAC → ACCEPTED
- invalid HMAC → REJECTED

### Current Status

IMPLEMENTED AND TESTED

---

## Threat 3 — Malformed Sensor Message

### Description

A malformed, incomplete or invalid message may be published to a legitimate sensor topic.

The monitoring system must not treat malformed data as a trusted sensor reading.

### Security Impact

- incorrect processing
- monitoring errors
- possible bypass of security logic

### Control

The monitor:

- decodes the MQTT payload
- validates JSON structure
- validates recognised sensor identity
- rejects unreadable or malformed data

### Test

Publish malformed or non-JSON data to the dissolved oxygen topic.

### Expected Result

The message is rejected and logged as a security alert.

### Current Status

IMPLEMENTED AND TESTED

---

## Threat 4 — Sensor Outage / Denial of Service

### Description

A sensor may stop transmitting because of:

- device failure
- network failure
- service outage
- malicious denial-of-service activity

For aquaculture operations, missing dissolved oxygen or temperature information may create a serious safety risk.

### Security Impact

- loss of availability
- delayed detection of dangerous conditions
- unsafe control decisions using stale data

### Control

The monitoring component maintains a separate last-valid-message timer for each expected sensor.

If no valid reading is received within the configured timeout, an outage alert is generated.

Current demonstration timeout:

`10 seconds`

### Test

Stop an active sensor while the monitoring system continues running.

### Expected Result

The affected sensor generates an independent outage alert.

Other active sensors must not hide the outage.

### Current Status

IMPLEMENTED AND TESTED

---

## Threat 5 — Fake Messages Masking a Real Outage

### Description

An attacker may attempt to keep a compromised or failed sensor appearing online by repeatedly sending invalid or tampered messages.

If invalid messages reset the sensor health timer, a genuine outage could remain undetected.

### Security Impact

- outage hidden from operators
- false availability status
- unsafe reliance on untrusted data

### Control

For the dissolved oxygen sensor, the health timer is updated only after successful HMAC verification.

Invalid HMAC messages do not count as valid sensor activity.

### Test

1. stop the legitimate DO sensor
2. continue publishing invalid-HMAC messages
3. observe the health timer

### Expected Result

The invalid messages are rejected and the DO outage alert still occurs.

### Current Status

IMPLEMENTED AND TESTED

---

## Threat 6 — Unsafe Automated Action During Data Loss

### Description

The control system may continue making automated decisions when required trusted sensor information is missing or invalid.

For example, a feeder or control process could continue operating despite loss of critical dissolved oxygen data.

### Security Impact

- harmful automated action
- stock loss
- unsafe control behaviour

### Control

A fail-safe controller will place the system into a safe state such as:

`SAFE/HOLD`

when required trusted sensor data is unavailable or invalid.

### Test

Simulate:

- critical sensor outage
- invalid sensor data
- loss of trusted readings

### Expected Result

The controller enters SAFE/HOLD and does not continue unsafe automated action.

### Current Status

PENDING IMPLEMENTATION

### Owner

Arnob

---

## Threat 7 — Credential or Secret Exposure

### Description

MQTT credentials or cryptographic keys committed directly to the GitHub repository could be exposed to unauthorised users.

### Security Impact

- sensor impersonation
- message forgery
- loss of authentication and integrity protection

### Control

Secrets should be stored outside committed source code using:

- environment variables
- ignored credential files
- configuration files excluded by `.gitignore`

Generated runtime logs should also be excluded where appropriate.

### Test

Review the repository for committed:

- MQTT passwords
- HMAC keys
- credential files

### Expected Result

Sensitive credentials are not stored in the repository.

### Current Status

PARTIALLY IMPLEMENTED / REVIEW REQUIRED

---

## Threat 8 — Inconsistent MQTT Topic Structure

### Description

Different sensors currently use different MQTT topic naming patterns.

Inconsistent topics may make:

- ACL configuration harder
- monitoring logic more complex
- integration more error-prone

### Control

Standardise sensor topics using a common structure such as:

```text
aquaculture/sensors/dissolved_oxygen
aquaculture/sensors/temperature
aquaculture/sensors/ph
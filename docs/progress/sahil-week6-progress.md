# Sahil Basnet — Implementation Progress to Week 6

## Scope of contribution

This document records Sahil Basnet's individual implementation work for the AQ-1 Secure and Resilient IoT Sensor-Control System for Coral Coast Aquaculture.

Sahil's current technical responsibility is the sensor-to-network security path: sensor simulation, MQTT communication, Mosquitto broker authentication, message integrity generation, controlled tamper testing, and the planned GNS3 network scale-up.

## Implemented work

### 1. Temperature sensor simulator

A Python temperature sensor simulator is implemented at:

`scripts/sensors/temperature_sensor.py`

The sensor:

- uses sensor identity `TEMP-001`
- represents pond `POND-01`
- generates simulated water-temperature readings
- classifies readings as `LOW`, `NORMAL`, or `HIGH`
- publishes a reading approximately every five seconds
- publishes to `aq1/pond1/temperature`

### 2. MQTT authentication

The temperature sensor authenticates to the Mosquitto MQTT broker using credentials loaded from environment variables:

- `AQ1_MQTT_USERNAME`
- `AQ1_MQTT_PASSWORD`

Broker configuration disables anonymous access on listener port `1883`.

The password file is intentionally excluded from GitHub through `.gitignore` and is not stored in the repository.

### 3. HMAC-SHA256 integrity protection

The temperature sensor generates an HMAC-SHA256 value for every message using a secret loaded from:

`AQ1_TEMP_HMAC_KEY`

The secret is not hard-coded in the committed Python source.

The canonical signed message format is:

`sensor_id|pond_id|sensor_type|value|unit|status|timestamp`

For the current temperature sensor this protects the sensor identity, pond identity, reading type, value, unit, status and timestamp from undetected modification.

### 4. Controlled temperature tamper test

A controlled security test is implemented at:

`scripts/security/temperature_tamper_test.py`

The test creates a legitimate HMAC for an original temperature reading and then deliberately changes the temperature value and status after signing. The original HMAC is retained, producing a message whose integrity check should fail at the verifier.

This creates repeatable malicious test traffic without changing the production sensor script.

### 5. MQTT authentication test

Broker authentication has been manually tested using MQTT subscriber clients.

Observed behaviour:

- a client using valid credentials can subscribe to the temperature topic and receive live messages
- a client with no credentials is rejected by the broker with `Connection Refused: not authorised`

This verifies that anonymous MQTT access is disabled for the current broker configuration.

## Integration with team components

The team monitoring component at `scripts/monitoring/monitor.py` now contains temperature HMAC verification using the same canonical field order as the temperature producer. The Week 6 security test plan records valid temperature HMAC and tampered temperature rejection as passing tests.

A remaining integration issue is that the monitoring client currently connects to MQTT without supplying broker credentials. The monitor therefore still needs MQTT authentication support to operate cleanly against the authenticated broker configuration in the final integrated environment.

The fail-safe `SAFE/HOLD` control path is a separate team integration task and is not claimed as part of Sahil's completed implementation.

## Evidence in Git history

Key Sahil commits include:

- `9a5216d` — `feat: add authenticated temperature sensor MQTT flow`
- `e98556c` — `feat: add HMAC protection and tamper test for temperature sensor`
- `fa4ac7c` — `feat: add HMAC integrity protection to temperature sensor`

Related team integration commits include:

- `283f698` — `feat: verify temperature HMAC and reject tampered readings`
- `816712f` — `Update Week_6_Security_Test_Plan.md`

## Current working data flow

```text
TEMP-001 temperature simulator
        |
        | MQTT username/password
        | HMAC-SHA256 protected payload
        v
Mosquitto MQTT broker :1883
        |
        +----> authorised MQTT subscriber
        |
        +----> monitoring component / security validation
```

## Current limitations

The current prototype is still mainly local-host based. Important next steps are:

- authenticate the monitoring client to the secure broker
- standardise MQTT topic naming across all sensors
- add topic-level access-control rules
- add TLS for transport confidentiality
- move the sensor, broker, monitoring and control components onto separate virtual network nodes
- build the planned GNS3 multi-pond topology
- add packet-capture evidence and network-segmentation tests
- integrate the monitoring trust decision with the `SAFE/HOLD` controller

## Planned GNS3 scale-up

The current local implementation will be used as the working baseline for a larger GNS3 deployment rather than being discarded.

The planned network will separate pond sensor networks, management/monitoring services and an attacker/test network. The first GNS3 milestone is to move the existing temperature sensor and Mosquitto broker onto different virtual network segments and prove that authenticated, HMAC-protected MQTT traffic crosses the routed topology successfully.

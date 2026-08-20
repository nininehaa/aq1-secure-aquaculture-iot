# Temperature Sensor MQTT Security Design

## Purpose

This document describes the security controls currently used for the AQ-1 temperature sensor path.

The goal is to protect two different things:

1. **Broker access** — only authorised MQTT clients should be able to connect.
2. **Message integrity** — a temperature reading that has been modified after signing should be detectable.

## Components

- Temperature sensor: `scripts/sensors/temperature_sensor.py`
- Mosquitto broker configuration: `configs/mosquitto/mosquitto.conf`
- Temperature tamper test: `scripts/security/temperature_tamper_test.py`
- Monitoring/verifier: `scripts/monitoring/monitor.py`
- MQTT topic: `aq1/pond1/temperature`

## MQTT authentication

The Mosquitto listener runs on TCP port `1883` with anonymous access disabled.

The temperature sensor reads its MQTT credentials from environment variables:

- `AQ1_MQTT_USERNAME`
- `AQ1_MQTT_PASSWORD`

Secrets are not committed to the repository. The local Mosquitto password file is ignored by Git.

### Authentication behaviour

```text
Client attempts MQTT connection
            |
            v
   Mosquitto checks credentials
        /               \
     valid             missing/wrong
       |                    |
       v                    v
   CONNECTED              REJECTED
```

A manual negative test confirmed that a subscriber without credentials is rejected with `Connection Refused: not authorised`.

## HMAC-SHA256 message integrity

After generating a temperature reading, `TEMP-001` creates an HMAC-SHA256 signature using a shared secret supplied through `AQ1_TEMP_HMAC_KEY`.

The exact canonical string is:

`sensor_id|pond_id|sensor_type|value|unit|status|timestamp`

Example structure:

`TEMP-001|POND-01|temperature|27.4|C|NORMAL|<timestamp>`

The HMAC is included in the JSON payload, but the shared secret itself is never sent in the MQTT message.

## Verification logic

The monitoring component reconstructs the same canonical string, recalculates HMAC-SHA256 using the same shared secret, and compares the calculated value with the HMAC carried in the message.

```text
received payload + shared secret
             |
             v
      calculate HMAC
             |
             v
compare with received HMAC
       /             \
    match           mismatch
      |                 |
      v                 v
   ACCEPT             REJECT
```

Only a temperature message with a valid HMAC should be treated as trusted sensor activity and allowed to reset the sensor outage timer.

## Controlled tamper test

`temperature_tamper_test.py` creates a valid signature for an original reading and then changes the value and status after the signature has been generated.

Current test values are:

- original value: `27.20 C`
- original status: `NORMAL`
- tampered value: `41.20 C`
- tampered status: `HIGH`

Because the message is modified after signing, the old HMAC does not match the changed payload. This allows the monitoring component to demonstrate tamper rejection.

## Security control separation

MQTT authentication and HMAC solve different problems.

| Control | Question answered |
| --- | --- |
| MQTT username/password | Is this client allowed to connect to the broker? |
| HMAC-SHA256 | Has the protected sensor message been changed? |

A client can therefore have valid MQTT credentials but still send a message that fails HMAC verification. This is why both controls are required.

## Current limitations and next controls

The current design is a prototype and still requires additional controls for the target high-scale architecture:

- MQTT authentication must be added to the monitoring client itself
- topic-level ACLs should restrict which sensor identity can publish to which topic
- TLS should protect MQTT traffic from passive observation
- replay protection should validate timestamp freshness, not only include the timestamp in the HMAC
- per-device keys and key rotation should be considered as the sensor fleet grows
- GNS3 network segmentation should separate pond, monitoring, management and attacker/test networks

## Security test evidence

The repository's Week 6 security test plan records:

- valid temperature HMAC: PASS
- tampered temperature message rejection: PASS
- broker rejection of unauthenticated MQTT access: completed by Sahil and documented in the Week 6 test-plan update

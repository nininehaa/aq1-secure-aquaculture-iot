# Dissolved-Oxygen Sensor Implementation

## Purpose

The dissolved-oxygen (DO) sensor simulator represents a water-quality sensor used by Coral Coast Aquaculture. Dissolved oxygen is important in aquaculture because low oxygen conditions can affect fish and prawn health.

The current simulator gives the team a repeatable source of DO readings for MQTT, integrity, monitoring, outage and tamper tests.

## Implementation File

`scripts/sensors/do_sensor.py`

## Current Configuration

| Item | Current value |
|---|---|
| Sensor ID | `sensor01` |
| Sensor type | `DO` |
| MQTT broker | `localhost` |
| MQTT port | `1883` |
| MQTT topic | `aquaculture/sensors/dissolved_oxygen` |
| Simulated range | `5.0` to `9.0` mg/L |
| Publish interval | approximately 5 seconds |
| Integrity method | HMAC-SHA256 |

## How It Works

The sensor follows this flow:

```text
Generate DO value
      |
      v
Create canonical string
sensor01|DO|value
      |
      v
Generate HMAC-SHA256
      |
      v
Create JSON payload
      |
      v
Publish through MQTT
```

A typical payload contains:

```text
sensor_id
sensor_type
value
hmac
```

## HMAC Integrity Protection

Before the message is published, the sensor creates the string:

`sensor_id|sensor_type|value`

For the current sensor this becomes similar to:

`sensor01|DO|7.25`

An HMAC-SHA256 value is generated from that string and included with the MQTT message.

The monitoring component recalculates the HMAC using the same format. If the message has been changed, the calculated HMAC will not match the received HMAC and the reading is rejected.

## Monitoring Integration

The monitoring component currently:

- recognises `sensor01` as the expected DO sensor
- checks the required DO fields
- verifies the HMAC before treating the reading as trusted
- rejects invalid or malformed DO messages
- updates the sensor last-seen time only after a valid reading
- raises an outage alert after the configured timeout
- records recovery when valid readings resume

## Testing Completed

The Week 6 security tests record the following as passing:

- valid DO HMAC accepted
- invalid/tampered DO HMAC rejected
- malformed DO message rejected
- DO sensor outage detected
- DO sensor recovery detected

See `testing/Week_6_Security_Test_Plan.md` for the recorded test results.

## Current Limitations

The current DO sensor is still part of the local prototype. Important limitations are:

- it connects to `localhost`
- it does not currently supply MQTT username/password credentials
- its HMAC secret is currently stored directly in the script
- MQTT transport is not yet protected with TLS
- it is not yet deployed on a separate GNS3 sensor node

These limitations are documented so that the current prototype is not confused with the final target design.

## Next Steps

Planned improvements include:

1. move the DO sensor to the standard authenticated MQTT configuration
2. move secrets out of source code
3. keep topic naming consistent with the agreed sensor structure
4. deploy the sensor on the GNS3 pond network
5. capture network traffic and verify firewall/ACL behaviour
6. integrate trusted DO status with the final `SAFE/HOLD` control logic

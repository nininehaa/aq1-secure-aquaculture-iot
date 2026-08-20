# Temperature Sensor Implementation

## Purpose

The temperature sensor simulator represents a water-temperature IoT device in the Coral Coast Aquaculture prototype.

The current implementation is located at:

`scripts/sensors/temperature_sensor.py`

## Identity

- Sensor ID: `TEMP-001`
- Pond ID: `POND-01`
- Sensor type: `temperature`
- Unit: `C`
- MQTT topic: `aq1/pond1/temperature`

## What the Sensor Does

Approximately every five seconds the sensor:

1. Generates a simulated water-temperature value.
2. Classifies the value as `LOW`, `NORMAL` or `HIGH`.
3. Creates a UTC timestamp.
4. Builds the canonical message used for integrity protection.
5. Generates an HMAC-SHA256 value.
6. Authenticates to the MQTT broker.
7. Publishes the JSON reading using MQTT QoS 1.

```text
Generate temperature
        |
        v
LOW / NORMAL / HIGH
        |
        v
Create timestamp
        |
        v
Generate HMAC-SHA256
        |
        v
Authenticate to Mosquitto
        |
        v
Publish MQTT message
```

## Message Format

A published reading contains:

- `sensor_id`
- `pond_id`
- `sensor_type`
- `value`
- `unit`
- `status`
- `timestamp`
- `hmac`

Example structure:

```json
{
  "sensor_id": "TEMP-001",
  "pond_id": "POND-01",
  "sensor_type": "temperature",
  "value": 27.4,
  "unit": "C",
  "status": "NORMAL",
  "timestamp": "<UTC timestamp>",
  "hmac": "<HMAC-SHA256 value>"
}
```

## MQTT Authentication

The sensor does not store MQTT credentials directly in the source file.

It reads:

- `AQ1_MQTT_USERNAME`
- `AQ1_MQTT_PASSWORD`

from environment variables.

If required credentials are missing, the program stops instead of attempting to run insecurely.

## HMAC Integrity Protection

The sensor reads the HMAC secret from:

`AQ1_TEMP_HMAC_KEY`

The committed source does not contain the secret itself.

The exact canonical signed message is:

`sensor_id|pond_id|sensor_type|value|unit|status|timestamp`

The monitoring component must use the same field order and separator to verify the HMAC correctly.

## Testing Completed

The following behaviour has been demonstrated:

- sensor starts with the required environment variables
- valid MQTT credentials allow connection to Mosquitto
- live temperature readings are repeatedly published
- an authorised subscriber receives the JSON messages
- each message contains an HMAC-SHA256 value
- the HMAC changes when the protected message changes

## Related Security Test

`scripts/security/temperature_tamper_test.py` creates a legitimate signed reading and then changes the value/status after signing. This produces a controlled message that should fail HMAC verification.

## Current Limitations / Next Work

- MQTT topic naming still needs to be standardised with the wider sensor topic structure.
- Topic-level ACL rules are not yet complete.
- TLS is not yet enabled for transport confidentiality.
- The sensor currently connects to a local broker and will later be moved to a GNS3 virtual pond network.

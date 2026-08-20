# Monitoring and Trust Verification

## Purpose

The monitoring component receives sensor messages and decides whether they can be treated as trusted.

Current implementation:

`scripts/monitoring/monitor.py`

## Expected Sensors

The monitor currently tracks:

- `sensor01` — dissolved oxygen
- `TEMP-001` — temperature

## What the Monitor Does

For each received message, the monitor checks the sensor identity and message format before accepting it.

For HMAC-protected sensors it recalculates the expected HMAC and compares it with the HMAC received in the message.

```text
Receive MQTT message
        |
        v
Identify sensor
        |
        v
Check required fields
        |
        v
Verify HMAC
        |
   +----+----+
   |         |
 valid     invalid
   |         |
accept     reject
   |         |
update     security alert
last seen
```

## Dissolved-Oxygen Verification

The DO path verifies the sensor identity, sensor type and HMAC before treating the reading as valid.

A malformed, unknown or invalid-HMAC DO message is rejected and does not reset the outage timer.

## Temperature Verification

The temperature path verifies these fields:

- sensor ID
- pond ID
- sensor type
- value
- unit
- status
- timestamp
- HMAC

The monitor reconstructs the same canonical string used by the temperature producer:

`sensor_id|pond_id|sensor_type|value|unit|status|timestamp`

If the calculated HMAC does not match the received HMAC, the temperature reading is rejected and a security alert is logged.

## Outage Detection

The monitor tracks the last valid reading time for each expected sensor.

Current timeout: `10` seconds.

If a sensor that previously provided valid data stops providing valid readings for longer than the timeout, the monitor records an outage alert.

Importantly, only a valid reading resets the timer. A tampered reading does not make an offline sensor appear healthy.

## Recovery Detection

If a sensor has been marked offline and later produces a valid reading, the monitor logs a recovery event and marks the sensor as online again.

## Logging

Security and availability events are printed and also written to `sensor.log` during execution.

Examples include:

- accepted valid reading
- HMAC verification failure
- malformed message rejection
- unknown sensor message
- outage alert
- recovery event

## Tests Completed

The Week 6 test plan records PASS results for:

- valid DO HMAC
- invalid/tampered DO HMAC
- malformed DO message
- DO outage and recovery
- temperature outage and recovery
- valid temperature HMAC
- tampered temperature rejection

## Current Integration Limitation

The monitoring MQTT client currently connects without supplying username/password credentials.

Because the secure broker disables anonymous access, the monitor still needs its own broker credentials for the fully integrated secure configuration.

This is a known integration task and is not hidden as completed work.

## Next Work

- add dedicated MQTT credentials for the monitor
- restrict monitor permissions to required subscription topics
- feed trusted/untrusted state into the control component
- expose monitoring information to the planned dashboard/Node-RED layer
- move the monitor to its own network segment in GNS3

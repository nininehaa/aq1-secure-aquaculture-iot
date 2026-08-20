# Security Design

## Purpose

The AQ-1 project is designed to stop false, modified or unavailable sensor data from being blindly trusted by an automated aquaculture control system.

The security design uses several controls because no single control solves every problem.

## Security Layers

```text
Sensor identity
    |
    v
MQTT authentication
    |
    v
Message integrity (HMAC)
    |
    v
Monitoring and validation
    |
    v
Outage / recovery detection
    |
    v
SAFE/HOLD control response
```

## Threats and Current Controls

| Threat | Example | Current/Planned Protection |
|---|---|---|
| Unauthorised MQTT access | Unknown client connects to broker | MQTT username/password authentication |
| Anonymous access | Client connects without credentials | Anonymous broker access disabled |
| Message tampering | 27 C changed to 41 C | HMAC-SHA256 verification |
| Sensor spoofing | Fake sensor claims a known identity | Broker authentication + sensor identity validation; stronger ACL/certificate work planned |
| Malformed data | Invalid/non-JSON message | Monitoring rejects malformed input |
| Sensor outage | Sensor silently stops publishing | Per-sensor timeout monitoring |
| False recovery | Invalid message resets outage state | Only valid trusted readings reset the timer |
| Unsafe automatic action | Bad data triggers equipment | `SAFE/HOLD` control integration planned |
| Network access between zones | IoT node reaches management services | GNS3 segmentation/firewall/ACL testing planned |
| Traffic disclosure | Attacker reads MQTT traffic | TLS planned |
| Replay of old valid data | Old signed packet is resent | Timestamp is included in temperature signed data; explicit freshness/replay checking is planned |

## MQTT Authentication

MQTT authentication answers:

**Is this client allowed to connect to the broker?**

The current Mosquitto configuration disables anonymous access. Valid `TEMP-001` credentials work and a no-credential test is rejected.

## HMAC-SHA256

HMAC answers a different question:

**Has the protected message changed?**

The temperature producer protects:

`sensor_id|pond_id|sensor_type|value|unit|status|timestamp`

The monitor recalculates the HMAC using the same agreed key and compares the result.

A mismatch means the message is not treated as trusted.

## Availability Monitoring

The monitor records the last valid reading for each expected sensor.

A sensor that stops producing valid data for more than the configured timeout is marked as unavailable.

This is important because a missing sensor is also a safety/security problem even when no obviously malicious message appears.

## Fail-Safe Principle

The final controller should not make a potentially harmful automatic decision when required trusted data is unavailable.

The planned response is:

- trusted data -> `NORMAL`
- invalid/tampered data -> reject and protect control path
- required sensor outage -> `SAFE/HOLD`
- valid recovery -> controlled return to normal

## Defence-in-Depth Direction

The final design will combine:

- device/client authentication
- topic access control
- HMAC message integrity
- TLS transport encryption
- input validation
- sensor availability monitoring
- network segmentation
- firewall rules
- logging/alerting
- fail-safe control behaviour

## Current Scope Boundary

The current prototype demonstrates several security controls locally, but the larger network-security design is not yet complete.

The next stage is GNS3 deployment so the team can test the same controls across separate sensor, broker, monitoring, management and attacker/test networks.

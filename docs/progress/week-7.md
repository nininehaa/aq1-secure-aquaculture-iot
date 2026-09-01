# Week 7 Project Progress

## Reporting period
24–30 August 2026

## Main focus
Week 7 moved the project from a localhost-only security prototype into the first working virtualised GNS3 temperature-to-monitor path, while also improving project traceability and documentation.

## Technical progress completed in Week 7

The team demonstrated the first working GNS3 temperature security slice using separate Alpine/Docker nodes:

```text
AQ1-TEMP-001-1
      |
      v
    Switch1
   /       \
  v         v
AQ1-Mosquitto-Broker-1    Neha-Monitor-1
```

`NAT3` was used temporarily for package installation/internet access. This is not yet the final Pond A routed/router-firewall topology.

### Neha monitoring work

`Neha-Monitor-1` was configured with Python, a virtual environment, `paho-mqtt`, and the project `monitor.py`.

The monitor successfully connected to the separate GNS3 Mosquitto broker and subscribed to the project MQTT topics.

### Broker and TEMP-001 integration

`AQ1-Mosquitto-Broker-1` was configured with Mosquitto and used as a separate MQTT service node.

`AQ1-TEMP-001-1` was configured with Python, `paho-mqtt`, the existing temperature producer, and the controlled tamper test.

A temporary anonymous listener was used only to prove the virtualised MQTT/HMAC path. Week 7 therefore does **not** claim that GNS3 broker authentication is already enforced.

## GNS3 security tests completed

### Valid temperature HMAC — PASS

The monitoring node received signed TEMP-001 readings and reported:

```text
ACCEPTED | Sensor: TEMP-001 | ... | HMAC: VALID
```

### Temperature outage — PASS

Stopping `temperature_sensor.py` caused:

```text
OUTAGE ALERT | Temperature sensor TEMP-001 unavailable | No valid reading for more than 10 seconds
```

### Temperature recovery — PASS

Restarting the producer caused:

```text
RECOVERY | Temperature sensor TEMP-001 is online again
```

followed by valid readings being accepted again.

### Temperature tamper rejection — PASS

The tamper test signed an original `27.2 C / NORMAL` reading, changed the payload to `41.2 C / HIGH` without recalculating the HMAC, and published the modified message through the GNS3 broker.

The monitor reported:

```text
SECURITY ALERT | Temperature reading rejected | Sensor: TEMP-001 | Reason: HMAC verification failed
```

Detailed evidence record: `docs/gns3/week7-temp-monitor-validation.md`.

## Engineering and documentation work completed

The repository was also expanded with shared engineering records so implementation, ownership and evidence can be reviewed more systematically:

- implementation-status source of truth
- requirements traceability matrix
- live project risk register
- weekly engineering-review template
- project evidence index improvements
- GNS3 deployment design and planned addressing
- consolidated security-test results
- implementation/setup/troubleshooting documentation
- project decisions and team-role documentation

## Current member workstreams

- **Sahil Basnet:** sensor/MQTT/network-security work, broker authentication, topic/ACL work and GNS3 network path.
- **Neha Thanait:** security monitoring, HMAC verification, outage/recovery, GNS3 security testing and verification evidence.
- **Md Monirul Haque Arnob:** SAFE/HOLD control and resilience integration.

## Week 7 outcome

Week 7 produced the first working virtualised TEMP-001 -> Mosquitto -> monitoring slice with valid HMAC acceptance, outage detection, recovery detection and tamper rejection.

The path still uses a temporary flat switch/NAT network and anonymous broker listener, so the full Pond A MVP is not complete.

## Remaining technical priorities for Week 8

- replace the temporary flat network with the planned Pond A routed/router-firewall path
- restore and enforce MQTT authentication in GNS3
- authenticate the monitoring client
- standardise MQTT topics and implement topic ACLs
- capture GNS3/Wireshark evidence
- move/validate DO in GNS3
- implement the pH path
- implement and integrate SAFE/HOLD

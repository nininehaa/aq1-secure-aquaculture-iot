# Week 8 Project Progress and Priorities

## Reporting period
31 August–6 September 2026

## Main focus
Week 8 started with a scope/documentation cleanup so all three team members were working from the same project plan, then moved into the first practical GNS3 implementation and security validation.

## Scope clarified
The project has **not** changed into a requirement to build three complete ponds now.

The current MVP is:

```text
ONE POND A GNS3 DEPLOYMENT

DO + Temperature + pH
        |
        v
MQTT / Mosquitto
        |
        v
Authentication + HMAC
        |
        v
Monitoring / outage detection
        |
        v
SAFE/HOLD control
        |
        v
Security and network evidence
```

The first practical GNS3 milestone begins with the existing `TEMP-001` path before adding DO and pH to the same Pond A deployment.

Pond B, Pond C, backup broker, larger attacker network, advanced Node-RED, TLS and redundancy/load testing are stretch/scale-up items after the MVP is stable.

## Repository cleanup completed at the start of Week 8

- created `docs/project-management/project-plan.md` as the current delivery plan
- updated the root README to show the one-Pond-A MVP clearly
- updated `docs/README.md` so the documentation has a clear reading order
- updated Issue #10 so the closed Week 6 security baseline no longer lists already-completed tests as pending
- clarified Issue #16 as the first one-Pond-A routed GNS3 milestone
- clarified Issue #17 as MQTT hardening for the Pond A MVP
- clarified Issue #18 as Arnob's required SAFE/HOLD workstream
- updated `AI-log.md` with later verified AI-assisted work and a rule that members record their own AI use

## Week 8 GNS3 implementation progress

A first working virtualised temperature security slice has now been demonstrated using separate Alpine/Docker nodes in GNS3:

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

### Neha monitoring node

`Neha-Monitor-1` was configured with Python, a virtual environment, `paho-mqtt`, and the project `monitor.py`.

The monitor successfully connected to the separate Mosquitto GNS3 broker and subscribed to the project MQTT topics.

### Mosquitto broker node

`AQ1-Mosquitto-Broker-1` was configured with Mosquitto 2.1.2 and used as a separate MQTT service node for the first GNS3 integration test.

A temporary anonymous listener was used only to prove the virtualised MQTT/HMAC path. Therefore Week 8 does **not** claim that GNS3 broker authentication is already enforced.

### TEMP-001 node

`AQ1-TEMP-001-1` was configured with Python, `paho-mqtt`, the existing temperature producer and the controlled temperature tamper test.

The producer sent signed temperature readings to the separate GNS3 broker.

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

Detailed evidence record: `docs/gns3/week8-temp-monitor-validation.md`.

## Current technical status

### Demonstrated locally and/or in GNS3
- DO MQTT/HMAC path locally
- temperature MQTT/HMAC path in GNS3
- valid temperature HMAC acceptance in GNS3
- temperature tamper rejection in GNS3
- temperature outage/recovery monitoring in GNS3
- separate GNS3 TEMP-001, Mosquitto and monitoring nodes

### Still in progress / pending
- replace temporary flat switch/NAT path with Pond A routed/router-firewall topology
- restore/enforce MQTT authentication in GNS3
- monitoring-client authentication
- topic standardisation and ACLs
- SAFE/HOLD implementation/integration
- pH sensor path
- DO migration/validation in GNS3
- GNS3/Wireshark packet-capture evidence

## Week 8 ownership

### Sahil Basnet
- monitoring-client/broker authentication integration support
- topic standardisation
- topic ACLs
- GNS3 routing/network setup and broker portability

### Neha Thanait
- monitoring node deployment in GNS3
- monitor-to-broker integration
- GNS3 temperature HMAC verification
- tamper rejection testing
- outage/recovery testing and evidence
- continue acceptance/security testing on the final routed path

### Md Monirul Haque Arnob
- implement SAFE/HOLD controller
- integrate trusted/outage state with control response
- test activation and controlled recovery

## Immediate next milestone

The first virtualised MQTT/HMAC slice is working. The next milestone is to turn it into the required Pond A security path by adding the missing network/security controls:

```text
TEMP-001 -> Pond A routed network/router-firewall -> authenticated Mosquitto -> authenticated monitor
```

with:

- valid credentials accepted
- missing/incorrect credentials rejected
- topic ACLs
- valid HMAC acceptance
- tamper rejection
- outage/recovery
- packet-capture evidence

After that, add DO/pH to Pond A and connect SAFE/HOLD for the full MVP.

## Week 8 rule
Do not mark planned work as complete. Update the existing project-plan, implementation-status, issues and test records when evidence changes instead of creating competing descriptions of the project.

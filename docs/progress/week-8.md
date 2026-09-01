# Week 8 Project Progress and Priorities

## Reporting period
31 August–6 September 2026

## Current position
Week 8 has just started.

The main technical result carried forward from Week 7 is the first working virtualised temperature security slice:

```text
AQ1-TEMP-001-1 -> Mosquitto broker -> Neha-Monitor-1
```

with valid HMAC acceptance, temperature outage detection, recovery detection and tamper rejection demonstrated in GNS3.

Detailed Week 7 evidence: `docs/gns3/week7-temp-monitor-validation.md`.

## Scope clarification at the start of Week 8

The project has **not** changed into a requirement to build three complete ponds now.

The current MVP remains:

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

Pond B, Pond C, backup broker, larger attacker network, advanced Node-RED, TLS and redundancy/load testing remain stretch/scale-up work after the MVP is stable.

## Documentation alignment completed at the start of Week 8

- created `docs/project-management/project-plan.md` as the current delivery plan
- clarified the one-Pond-A MVP in the root README and documentation index
- aligned Issue #10 with the completed Week 6 baseline
- clarified Issue #16 as the GNS3 Pond A deployment task
- clarified Issue #17 as MQTT hardening work
- clarified Issue #18 as Arnob's SAFE/HOLD workstream
- updated the AI-use record and documentation rules
- corrected the weekly timeline so the first GNS3 TEMP-001 validation is recorded as Week 7 work

## Week 8 technical priorities

### Sahil Basnet

- restore and enforce broker-side MQTT authentication in GNS3
- authenticate the monitoring client
- standardise MQTT topics
- implement topic ACLs
- develop the Pond A routed/router-firewall network path

### Neha Thanait

- repeat monitoring/security verification after authentication and routing are added
- capture evidence for valid, tampered, outage and recovery behaviour on the hardened path
- support packet-capture/Wireshark acceptance evidence
- move/validate the DO monitoring path in GNS3

### Md Monirul Haque Arnob

- implement SAFE/HOLD controller behaviour
- consume trusted/outage state from the verification layer
- test activation and controlled recovery

## Immediate Week 8 milestone

Build from the Week 7 working slice toward:

```text
TEMP-001
   |
Pond A routed network / router-firewall
   |
authenticated Mosquitto
   |
authenticated monitoring node
```

and demonstrate:

- valid credentials accepted
- missing/incorrect credentials rejected
- authorised topic access
- valid HMAC acceptance
- tamper rejection
- outage/recovery
- packet-capture evidence

## Still pending for the full MVP

- final Pond A routed network
- enforced GNS3 MQTT authentication and ACLs
- packet capture/Wireshark evidence
- DO validation in GNS3
- pH implementation/validation
- SAFE/HOLD implementation and end-to-end integration

## Week 8 rule

Do not mark planned work as complete. Update the project plan, implementation status, issues and test evidence only when the corresponding implementation has been run and demonstrated.

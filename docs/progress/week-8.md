# Week 8 Project Progress and Priorities

## Reporting period
31 August–6 September 2026

## Main focus
Week 8 starts with a scope and documentation cleanup so all three team members are working from the same project plan before further GNS3 and control integration.

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

The first practical GNS3 milestone may begin with the existing `TEMP-001` path before adding DO and pH to the same Pond A deployment.

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

## Current technical status

### Tested locally
- DO MQTT/HMAC path
- temperature MQTT/HMAC path
- valid/tampered HMAC verification
- malformed-message rejection
- independent outage/recovery monitoring
- temperature broker authentication and no-credential rejection

### In progress / pending
- monitoring-client MQTT authentication
- topic standardisation and ACLs
- SAFE/HOLD implementation/integration
- first routed GNS3 Pond A path
- pH sensor path
- GNS3/Wireshark security-test evidence

## Week 8 ownership

### Sahil Basnet
- monitoring-client/broker authentication integration support
- topic standardisation
- topic ACLs
- GNS3 routing/network setup and broker portability

### Neha Thanait
- monitor integration with the secured broker
- GNS3 security verification and acceptance tests
- HMAC/tamper/outage/recovery evidence across the routed path

### Md Monirul Haque Arnob
- implement SAFE/HOLD controller
- integrate trusted/outage state with control response
- test activation and controlled recovery

## Immediate next milestone
The team should next demonstrate:

```text
TEMP-001 -> Pond A GNS3 network -> router/firewall -> Mosquitto -> authenticated monitor
```

with valid MQTT authentication, HMAC acceptance, tamper rejection, outage/recovery and packet-capture evidence.

After that, complete the Pond A sensor scope and connect SAFE/HOLD for the full MVP.

## Week 8 rule
Do not mark planned work as complete. Update the existing project-plan, implementation-status, issues and test records when evidence changes instead of creating competing descriptions of the project.

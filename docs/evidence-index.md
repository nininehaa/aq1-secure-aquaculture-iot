# Project Evidence Index

## Purpose

This file connects project documentation to actual code, configuration, tests and Git history so that project reviews and demonstrations can move from a requirement to the corresponding implementation and evidence.

## Current Implementation Evidence

| Area | Main evidence | Status |
|---|---|---|
| Project overview | `README.md`, `docs/project-overview.md` | Current |
| Implementation status | `docs/project-management/implementation-status.md` | Current source of truth |
| Requirements traceability | `docs/project-management/requirements-traceability.md` | Current |
| Risk register | `docs/project-management/risk-register.md` | Live |
| System architecture | `docs/architecture/system-architecture.md`, `docs/architecture/current-week6-architecture.md` | Current + planned scale-up |
| Dissolved-oxygen sensor | `scripts/sensors/do_sensor.py`, `docs/implementation/dissolved-oxygen-sensor.md` | Implemented locally |
| Temperature sensor | `scripts/sensors/temperature_sensor.py`, `docs/implementation/temperature-sensor.md` | Implemented locally |
| pH sensor | Project scope/design | Pending implementation |
| Mosquitto broker | `configs/mosquitto/mosquitto.conf`, `docs/implementation/mqtt-broker.md` | Implemented locally |
| Temperature MQTT authentication | sensor/broker implementation and Week 6 authentication test | PASS for tested local flow |
| DO HMAC generation | `scripts/sensors/do_sensor.py` | Implemented |
| Temperature HMAC generation | `scripts/sensors/temperature_sensor.py` | Implemented |
| Monitoring / HMAC verification | `scripts/monitoring/monitor.py`, `docs/implementation/monitoring.md` | Implemented locally |
| Temperature tamper test | `scripts/security/temperature_tamper_test.py` | Implemented |
| Sensor outage/recovery | `scripts/monitoring/monitor.py`, Week 6 tests | PASS locally |
| SAFE/HOLD control | `docs/implementation/failsafe-controller.md`, Issue #18 | Pending integration |
| GNS3 deployment | `docs/gns3/gns3-design.md`, Issue #16 | In progress |
| GNS3 addressing | `docs/gns3/network-addressing.md` | Planned until applied to running nodes |

## Week 6 Test Evidence

Primary test record:

`testing/Week_6_Security_Test_Plan.md`

Consolidated summary:

`testing/security-test-results.md`

Recorded results include:

- valid DO HMAC — PASS
- invalid DO HMAC — PASS
- malformed DO message — PASS
- DO outage — PASS
- DO recovery — PASS
- temperature outage — PASS
- temperature recovery — PASS
- missing MQTT credentials rejected — PASS
- valid temperature HMAC — PASS
- tampered temperature reading rejected — PASS
- SAFE/HOLD activation — PENDING

These are local-prototype results unless the individual test record explicitly states otherwise. GNS3 tests must be recorded separately when the virtualised path is executed.

## Workstream Evidence

### Sensor / MQTT / Network Security

Relevant evidence includes:

- `scripts/sensors/`
- `configs/mosquitto/`
- `docs/implementation/temperature-sensor.md`
- `docs/implementation/mqtt-broker.md`
- `docs/security/temperature-mqtt-security.md`
- Issue #17 — MQTT authentication, topic standardisation and ACL preparation
- Issue #16 — shared GNS3 network-scale work

### Security Monitoring and Verification

Relevant evidence includes:

- `scripts/monitoring/monitor.py`
- `docs/implementation/monitoring.md`
- Week 5 and Week 6 monitoring/security tests
- DO and temperature HMAC verification
- per-sensor outage and recovery detection

### Control and Resilience

Relevant evidence includes:

- `docs/implementation/failsafe-controller.md`
- Issue #18 — SAFE/HOLD fail-safe control

SAFE/HOLD implementation/test remains pending and must not be marked complete until working evidence is committed.

## Configuration and Secret Handling Evidence

Mosquitto configuration:

`configs/mosquitto/mosquitto.conf`

Local password/secrets files should not be committed. Sensor/broker credentials and HMAC secrets should be supplied through environment variables or local secret/configuration mechanisms excluded from version control.

## Project Management Evidence

- `docs/project-management/implementation-status.md` — current implementation truth
- `docs/project-management/requirements-traceability.md` — requirement-to-evidence mapping
- `docs/project-management/risk-register.md` — live project/security risk register
- `docs/project-management/weekly-review-template.md` — repeatable weekly engineering review format
- `docs/project-decisions.md` — architecture/design decisions and reasons
- GitHub issues / project board — ownership and current work
- Teams — discussion/decision context where required by the unit workflow

## Evidence Still Needed

Add these only after the relevant implementation is actually completed:

- GNS3 topology screenshots/exported project evidence
- actual node IP assignments verified from running nodes
- routing/firewall configuration and connectivity tests
- MQTT ACL configuration and authorised/unauthorised tests
- monitoring-client authenticated MQTT test in GNS3
- packet captures from the routed GNS3 path
- pH sensor implementation and security tests
- SAFE/HOLD implementation, activation and recovery evidence
- Node-RED/dashboard screenshots or exported flows if implemented
- TLS configuration and verification if implemented
- resilience/failover evidence if a backup broker becomes part of the tested scope

## Evidence Rule

A screenshot without context is not enough, and code without execution is not enough. Each important feature should be traceable through:

`requirement -> owner/issue -> code/config -> running implementation -> test -> actual result -> evidence`

Planned features must remain marked **Planned/Pending** until that chain exists.

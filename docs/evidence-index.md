# Project Evidence Index

## Purpose

This file connects the project documentation to the actual code, configuration, tests and Git history. It is intended to make project reviews and demonstrations easier.

## Current Implementation Evidence

| Area | Main evidence | Status |
|---|---|---|
| Project overview | `README.md`, `docs/project-overview.md` | Current |
| System architecture | `docs/architecture/system-architecture.md`, `docs/architecture/current-week6-architecture.md` | Current + planned scale-up |
| Dissolved-oxygen sensor | `scripts/sensors/do_sensor.py`, `docs/implementation/dissolved-oxygen-sensor.md` | Implemented locally |
| Temperature sensor | `scripts/sensors/temperature_sensor.py`, `docs/implementation/temperature-sensor.md` | Implemented locally |
| Mosquitto broker | `configs/mosquitto/mosquitto.conf`, `docs/implementation/mqtt-broker.md` | Implemented locally |
| Temperature MQTT authentication | `scripts/sensors/temperature_sensor.py`, Week 6 TC-W6-08 | PASS for tested producer/subscriber flow |
| DO HMAC generation | `scripts/sensors/do_sensor.py` | Implemented |
| Temperature HMAC generation | `scripts/sensors/temperature_sensor.py` | Implemented |
| Monitoring / HMAC verification | `scripts/monitoring/monitor.py`, `docs/implementation/monitoring.md` | Implemented |
| Temperature tamper test | `scripts/security/temperature_tamper_test.py` | Implemented |
| Sensor outage/recovery | `scripts/monitoring/monitor.py`, Week 6 tests | PASS |
| SAFE/HOLD control | `docs/implementation/failsafe-controller.md`, Issue #18 | Pending integration |
| GNS3 deployment | `docs/gns3/gns3-design.md`, Issue #16 | Planned / in progress |
| GNS3 addressing | `docs/gns3/network-addressing.md` | Planned |

## Week 6 Test Evidence

The main recorded test file is:

`testing/Week_6_Security_Test_Plan.md`

A shorter consolidated summary is available at:

`testing/security-test-results.md`

Current recorded results include:

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

## Sahil Basnet Evidence

Sahil's current contribution is documented in:

- `docs/progress/sahil-week6-progress.md`
- `docs/implementation/temperature-sensor.md`
- `docs/implementation/mqtt-broker.md`
- `docs/security/temperature-mqtt-security.md`
- `docs/gns3/gns3-design.md`

Key technical commits include:

- `9a5216d` — authenticated temperature sensor MQTT flow
- `e98556c` — HMAC protection and temperature tamper test
- `fa4ac7c` — HMAC integrity protection to temperature sensor

Current Sahil-owned or shared work items include:

- Issue #17 — MQTT authentication, topic standardisation and ACL preparation
- Issue #16 — GNS3 virtualised AQ-1 topology (shared network-scale work)

## Neha Thanait Evidence

Neha's monitoring/security-validation contribution is represented by:

- `scripts/monitoring/monitor.py`
- `docs/implementation/monitoring.md`
- Week 5 and Week 6 monitoring/security tests
- DO and temperature HMAC verification
- outage and recovery detection

## Md Monirul Haque Arnob Evidence

Arnob's control/resilience area is represented by:

- `docs/implementation/failsafe-controller.md`
- Issue #18 — SAFE/HOLD fail-safe control

The SAFE/HOLD implementation/test is currently recorded as pending and should only be marked complete after working evidence is committed.

## Configuration and Secret Handling Evidence

The repository contains the Mosquitto configuration at:

`configs/mosquitto/mosquitto.conf`

The local password file is intentionally excluded by `.gitignore` and should not be committed.

The secure temperature sensor reads MQTT credentials and its HMAC secret from environment variables instead of storing them directly in the committed Python source.

## Documentation Evidence

Project documentation is indexed from:

`docs/README.md`

Important documentation includes:

- project overview
- team roles
- architecture
- implementation guides
- security design and threat model
- project decisions
- troubleshooting log
- setup instructions
- weekly progress
- test plans/results
- GNS3 design and addressing

## Evidence Still Needed Later

The following evidence should be added when those stages are actually completed:

- GNS3 topology screenshots/files
- actual GNS3 IP assignments
- firewall configuration and tests
- MQTT ACL configuration and tests
- monitoring-client authenticated MQTT test
- TLS configuration and packet capture
- Node-RED/control screenshots or exported flows
- SAFE/HOLD test evidence
- primary/backup broker resilience test

The project should not mark these items as completed until actual implementation and test evidence exists.

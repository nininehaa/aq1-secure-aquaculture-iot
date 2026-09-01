# AQ-1 Current Project Plan

## Purpose

This document is the team's current delivery plan. It separates the **main implementation target (MVP)** from **later scale-up/stretch work** so that the team, tutor and reviewers can clearly see what we are building first, who owns each part, what is already working, and what remains.

The project has not changed into a requirement to build three complete ponds. The immediate target is to build **one secure Pond A path in GNS3** and prove the full security and fail-safe workflow end to end. Additional ponds are a later scale-up option after the MVP is stable.

## Project Goal

Build a secure and resilient aquaculture sensor-control system for Coral Coast Aquaculture that protects:

- sensor/client identity
- sensor-message integrity
- availability of trusted sensor data
- safe control behaviour when trusted data is invalid or unavailable

The project scope includes three main sensor types:

1. dissolved oxygen (DO)
2. temperature
3. pH

The current local prototype has working DO and temperature paths. The pH path remains to be implemented and tested.

## Current Position

The strongest working local prototype is:

```text
DO / Temperature producer
        |
        v
Mosquitto MQTT broker
        |
        v
Security monitor / HMAC verification
        |
        v
Trusted / rejected / outage decision
```

Current working evidence includes MQTT communication, temperature broker authentication, HMAC-SHA256 for DO and temperature, tamper rejection, malformed-message rejection, independent outage detection and recovery detection.

This localhost prototype is the security baseline. It is not the final deployment target.

## Main MVP — What We Must Build First

The main implementation target is **one Pond A GNS3 deployment**.

```text
POND A

DO endpoint --------+
Temperature endpoint +----> Pond A network
pH endpoint --------+             |
                                  v
                           Router / Firewall
                                  |
                                  v
                          Mosquitto MQTT broker
                                  |
                                  v
                     Monitoring / Trust Validation
                                  |
                                  v
                         SAFE/HOLD Controller
```

The first GNS3 milestone may begin with the existing temperature path before the other sensor types are added.

### MVP acceptance criteria

The MVP is considered demonstrated only when the team can show:

1. At least one sensor endpoint runs on a separate GNS3 node/endpoint rather than relying only on localhost.
2. The endpoint reaches Mosquitto across the routed Pond A network.
3. Correct MQTT credentials are accepted and missing/incorrect credentials are rejected.
4. A valid HMAC-protected reading reaches the monitoring component and is accepted.
5. A tampered reading is rejected.
6. Stopping a required sensor produces an independent outage alert.
7. SAFE/HOLD is activated when trusted required data is unavailable or invalid.
8. Valid recovery is detected and the controller returns through a controlled recovery path.
9. GNS3/Wireshark evidence shows the real network path and relevant security tests.
10. The implementation, configuration, test results and limitations are documented in GitHub.

## Technical Ownership

### Sahil Basnet — Sensor, MQTT and Network Security

Primary responsibilities:

- sensor publishing path, especially temperature producer
- Mosquitto configuration
- MQTT client authentication
- topic standardisation and topic ACLs
- HMAC generation on the producer side
- controlled temperature tamper traffic
- GNS3 routing/network segmentation work
- packet-capture/network-security testing

### Neha Thanait — Monitoring, Trust Validation and Security Testing

Primary responsibilities:

- security monitoring component
- DO and temperature HMAC verification
- malformed/tampered message rejection
- per-sensor outage and recovery detection
- security event logging/alerts
- acceptance/security testing
- verification evidence for the integrated GNS3 path

### Md Monirul Haque Arnob — Control and Resilience

Primary responsibilities:

- SAFE/HOLD controller
- simulated/virtual actuator behaviour
- response to invalid or unavailable trusted data
- controlled recovery after trusted data returns
- Node-RED control integration where used
- control/resilience testing

### Shared integration responsibility

All three members are responsible for ensuring their parts work together as one end-to-end system. Each member should commit and explain their own technical evidence from their own GitHub account/branch where practical.

## Delivery Order

| Phase | Main work | Owner(s) | Current status |
|---|---|---|---|
| 1. Local secure MQTT baseline | DO/temp -> MQTT -> verification -> outage/tamper decisions | Sahil + Neha + Arnob earlier HMAC work | Tested locally |
| 2. MQTT hardening | monitor authentication, topic standardisation, topic ACLs | Sahil | In progress |
| 3. SAFE/HOLD integration | trusted/outage state -> safe control response | Arnob | Pending integration |
| 4. First routed GNS3 path | TEMP-001 -> Pond A -> router/firewall -> Mosquitto -> monitor | Team; Sahil network lead | In progress / design prepared |
| 5. GNS3 security tests | valid auth, bad/no auth, HMAC tamper, outage/recovery, packet capture | Neha + Sahil | Pending |
| 6. Complete Pond A sensor scope | add/validate DO, temperature and pH paths | Team | pH pending |
| 7. End-to-end control test | sensor -> broker -> verifier -> SAFE/HOLD -> recovery | All; Arnob control lead | Pending |
| 8. Final reproducibility/evidence | setup, configs, test results, traceability, live demo | All | Ongoing |

## Stretch / Scale-Up Work — Only After MVP Is Stable

The following are **not the immediate requirement for the first working GNS3 deployment**. They are later scale-up/stretch options:

- Pond B and Pond C
- backup/secondary MQTT broker
- larger attacker/test network
- additional feeder/sensor identities
- broader Node-RED dashboard functionality
- TLS deployment and stronger key-management work
- broker failover/redundancy experiments
- larger load/scale testing

These items must remain marked **Planned** or **In progress** until they are actually implemented, tested and evidenced.

## Documentation and Evidence Rules

For every meaningful feature, the team should maintain this chain:

```text
requirement
   -> owner / issue
   -> code or configuration
   -> running implementation
   -> test
   -> observed result
   -> evidence
   -> documentation
```

A feature is not complete because code exists. For this project, completion means:

**built + configured + run + tested + evidenced + documented**

## GitHub Working Rule

Use these files for different questions:

- `README.md` — What is the project and what is the current high-level status?
- `docs/project-management/project-plan.md` — What are we building, in what order, and what is MVP vs stretch?
- `docs/project-management/implementation-status.md` — What actually works today?
- `docs/team-roles.md` — Who owns each technical area?
- `docs/project-management/requirements-traceability.md` — Which requirement maps to which implementation/test/evidence?
- `testing/` — What was actually tested and what passed/failed?
- `docs/progress/` — What changed each week?

If these records disagree, update the stale record rather than creating another competing version of the project plan.

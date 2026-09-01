# Secure and Resilient IoT Sensor-Control System

## Client
Coral Coast Aquaculture

## Team Members
- Neha Thanait
- Sahil Basnet
- Md Monirul Haque Arnob

## Project Scenario
AQ-1 — IoT/Sensor Security for a Prawn and Barramundi Farm

## Project Goal
This project is building a secure and resilient aquaculture IoT sensor-control system that protects sensor identity, message integrity, trusted-data availability and safe control behaviour.

The project scope includes three main sensor types:

- dissolved oxygen (DO)
- temperature
- pH

The current local prototype has working DO and temperature paths. The pH path is still pending implementation/testing.

## Main Implementation Target (MVP)

The immediate target is **one secure Pond A deployment in GNS3**, not three complete ponds.

```text
Pond A sensor endpoints
(DO + Temperature + pH)
          |
          v
Pond A virtual network
          |
          v
Router / Firewall
          |
          v
Mosquitto MQTT broker
          |
          v
Security monitoring / trust validation
          |
          v
SAFE/HOLD control
```

The first GNS3 milestone may start with the existing `TEMP-001` path and then add the remaining Pond A sensor paths.

The current Python producers are the local security-prototype/test baseline. The final project should move the working security path onto separated GNS3 nodes/endpoints so the result is not only a localhost sensor simulation.

For the full delivery order, ownership and acceptance criteria, see the [current project plan](docs/project-management/project-plan.md).

## Current Working Prototype

Implemented/tested locally in the repository:

- dissolved-oxygen and temperature producer paths
- Eclipse Mosquitto MQTT messaging
- authenticated MQTT path for temperature sensor `TEMP-001`
- anonymous MQTT access disabled in the current secure broker configuration
- HMAC-SHA256 generation for DO and temperature readings
- HMAC verification for DO and temperature readings
- controlled temperature tamper-test client
- malformed/tampered message rejection
- independent sensor outage and recovery monitoring
- Week 6 security tests and recorded results
- technical/security/project documentation

Current integration work still includes:

- MQTT authentication support for the monitoring client
- standardised MQTT topic structure and topic ACLs
- pH implementation and security tests
- `SAFE/HOLD` fail-safe controller integration
- first routed GNS3 Pond A deployment
- GNS3/Wireshark network evidence

## Current Data Flow

```text
Local DO / Temperature prototype
          |
          v
Mosquitto MQTT broker
          |
          v
Security monitoring / HMAC verification
          |
          v
Trusted / rejected / outage state
          |
          v
SAFE/HOLD control integration (pending)
```

## Stretch / Scale-Up Direction

Only after the one-Pond-A MVP is stable, the design may be expanded with:

- Pond B and Pond C
- backup MQTT broker
- larger attacker/test network
- additional sensor/feeder identities
- broader Node-RED dashboard/control functionality
- TLS and stronger key management
- broker failover/redundancy tests
- larger scale/load tests

These are **future scale-up/stretch goals**, not the immediate first GNS3 requirement.

## Main Technologies

- Python
- Eclipse Mosquitto MQTT
- HMAC-SHA256
- GitHub and GitHub Projects
- Microsoft Teams
- Wireshark
- GNS3
- Node-RED for planned monitoring/control integration

## Team Technical Focus

- **Sahil Basnet:** sensor/MQTT/network security, temperature producer, broker authentication, HMAC generation, MQTT ACL/topic work, GNS3 network integration
- **Neha Thanait:** sensor trust validation, HMAC verification, outage/recovery monitoring, security logging/alerts and acceptance/security testing
- **Md Monirul Haque Arnob:** control/resilience integration, `SAFE/HOLD`, Node-RED/control integration and virtual actuator behaviour

## Where to Start in the Documentation

1. [Current project plan](docs/project-management/project-plan.md) — what we are building, in what order, and MVP vs stretch
2. [Implementation status](docs/project-management/implementation-status.md) — what actually works today
3. [Team roles and ownership](docs/team-roles.md) — who owns each technical area
4. [Documentation index](docs/README.md) — all supporting documentation
5. [Requirements traceability](docs/project-management/requirements-traceability.md) — requirement-to-implementation/test mapping
6. [Security test results](testing/security-test-results.md) — recorded security testing

## Demonstration Goals

For the MVP, the team should ultimately demonstrate:

1. a sensor endpoint communicating across the routed GNS3 Pond A path
2. valid MQTT credentials accepted and missing/incorrect credentials rejected
3. a valid HMAC-protected reading accepted
4. a tampered reading rejected
5. a required sensor outage detected independently
6. `SAFE/HOLD` activated when trusted data is unavailable or invalid
7. controlled recovery when valid trusted data returns
8. GNS3/Wireshark evidence showing the actual network path

## Documentation Rule

For each meaningful implementation change, record:

1. why the work was needed
2. what was implemented or changed
3. how it works
4. how it was configured/run
5. how it was tested
6. the observed result
7. where the evidence is located
8. what remains

A feature is complete only when it is **built + configured + run + tested + evidenced + documented**.

Planned and stretch items must remain clearly marked so the repository does not overstate project progress.

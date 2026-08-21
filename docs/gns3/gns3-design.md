# GNS3 Deployment Design

## Status

**Planned / in progress.**

This document describes the next network-scale stage of the AQ-1 project. It does not claim that the full GNS3 topology is already implemented.

## Why GNS3 Is Being Added

The current prototype proves the main security functions locally, but most components still run on the same computer using `localhost`.

That is useful for early development, but it does not represent a realistic aquaculture network with separate pond sensors, monitoring systems, routers, firewalls and attacker/test devices.

GNS3 will be used to turn the working local prototype into a virtual network where the security controls can be tested across real network paths.

## Current Local Prototype

```text
Temperature sensor ----\
                       \
DO sensor --------------> Mosquitto on localhost
                              |
                              v
                         Monitoring
```

This proves application-level behaviour but gives limited evidence for segmentation, routing and firewall controls.

## First GNS3 Milestone

The first practical goal is intentionally small and testable:

```text
TEMP-001 sensor node
        |
        v
Pond A virtual network
        |
        v
Router / firewall
        |
        v
Mosquitto broker node
        |
        v
Monitoring node
```

The existing Python temperature sensor, broker configuration and HMAC logic will be reused instead of being replaced.

## Target Components

The larger topology is planned to include:

### Pond Networks

- Pond A sensor network
- Pond B sensor network
- Pond C sensor network
- temperature sensors
- dissolved-oxygen sensors
- later pH/feeder or other simulated devices

### Core / Security Components

- router/firewall
- primary MQTT broker
- later backup MQTT broker
- monitoring/security node
- management network
- attacker/test network

### Control Components

- Node-RED or equivalent control-processing node
- simulated aerator/pump/feeder behaviour
- `SAFE/HOLD` controller integration

## Security Goals

The GNS3 environment will be used to test controls that cannot be properly demonstrated with every component on `localhost`.

Planned tests include:

- routing between pond and broker networks
- blocking unauthorised network paths
- MQTT authentication across different nodes
- topic access-control rules
- HMAC-protected messages crossing the network unchanged
- attacker/test traffic from a separate network
- Wireshark/GNS3 packet capture
- sensor outage behaviour across the virtual network
- later broker failover and resilience testing

## First Acceptance Criteria

The first GNS3 stage will be considered working when:

1. the GNS3 project starts successfully
2. `TEMP-001` runs on a separate virtual node or host-connected endpoint
3. the Mosquitto broker is reachable across the virtual network instead of only through `localhost`
4. correct MQTT credentials are accepted
5. missing or incorrect credentials are rejected
6. HMAC-protected temperature messages arrive correctly
7. traffic can be captured and inspected
8. topology/configuration evidence is saved in the repository

## Planned Expansion

After the first path works, the topology can be expanded with:

- more pond networks
- multiple sensor identities
- management and monitoring VLANs
- dedicated security/test network
- topic ACLs
- firewall policy
- TLS
- primary and backup MQTT brokers
- Node-RED/control node
- `SAFE/HOLD` integration
- scale/load tests using multiple simulated sensors

## Evidence To Record

When implementation begins, each stage should include:

- topology screenshot
- node list
- IP-address table
- router/firewall configuration
- commands used
- packet-capture screenshot or file
- test case
- expected result
- actual result
- PASS/FAIL status
- Git commit or issue reference

This will keep the GNS3 work reproducible and suitable for project demonstration.

# AQ-1 GNS3 Network Deployment

## Overview

This document describes the AQ-1 demonstration network used to connect simulated water-quality sensors, a security gateway, an attacker test node, and the external MQTT messaging service. It documents the implemented network separately from proposed future improvements.

The deployment supports the project's application-layer security testing: HMAC-SHA256 message verification, replay detection, sensor availability monitoring, and reporting to the Node-RED monitoring workflow.

## Network Architecture

```text
                         NAT1
                          |
                       Switch1
                    /   /  \   \
                   /   /    \   \
             Attacker1 DO-001 PH-001 AQ1-Gateway
               .133     .138   .139     .140
                 \       |      |       /
                  192.168.127.0/24

      Internet / external MQTT service:
                 broker.hivemq.com
                          |
                  AQ1-Monitor (host PC)
                      Node-RED
```

`Switch1` provides Layer 2 connectivity among the four virtual endpoints. `NAT1` provides an outbound path to the external MQTT broker. The MQTT service is a public HiveMQ broker, **not** a Mosquitto broker deployed inside GNS3. `AQ1-Monitor` is the host-side monitoring environment, not a fifth endpoint on the GNS3 subnet.

The physical temperature-sensor component is part of the wider AQ-1 prototype and is not represented as an additional GNS3 node in this topology.

For host addresses, refer to [network-addressing.md](network-addressing.md).

## Deployed Components

| Component | Role |
|---|---|
| `DO-001` | Python-based simulated dissolved-oxygen sensor publisher |
| `PH-001` | Python-based simulated pH sensor publisher |
| `AQ1-Gateway` | Python MQTT subscriber performing integrity and replay checks |
| `Attacker1` | Controlled security-testing endpoint |
| `Switch1` | Local virtual network connectivity |
| `NAT1` | Outbound connectivity to external services |
| HiveMQ public broker | MQTT message exchange between project components |
| `AQ1-Monitor` | Host-PC Node-RED monitoring and dashboard environment |

## Message Processing

1. Sensor applications generate dissolved-oxygen and pH readings and publish MQTT messages.
2. The public HiveMQ broker distributes messages to subscribed clients.
3. The AQ-1 Gateway subscribes to the relevant sensor topics and validates messages before treating readings as trusted.
4. HMAC-SHA256 checks message authenticity and integrity; sequence checks support replay detection.
5. Accepted readings and security events are processed by the project's monitoring workflow.
6. Node-RED provides visual monitoring and alerts. Database configuration and persistence should be documented alongside the Node-RED flow, rather than assumed from the network configuration.

### Confirmed Gateway MQTT Configuration

| Setting | Value |
|---|---|
| Broker | `broker.hivemq.com` |
| Transport | MQTT over WebSockets |
| TCP port | `8000` |
| WebSocket path | `/mqtt` |
| Gateway subscription | `aquaculture/sensors/#` |

The Alpine Gateway connection was validated by a successful MQTT connection acknowledgement (`CONNACK` return code `0`). Port `8000` describes the confirmed Gateway connection; other project clients may use their own configured transport. Earlier experiments with ports `1883` and `8883` are not the final Gateway configuration.

## Security Scope

The project uses HMAC-SHA256 to reject messages that fail keyed integrity verification. Replay validation checks previously used or stale message sequences. Monitoring logic also addresses missing sensor updates. These are **application-layer** controls: they do not imply that the underlying network is segmented or that the public broker enforces project-specific access-control lists.

`Attacker1` shares the same `192.168.127.0/24` network as the sensors and Gateway. It is a controlled test host, **not** an isolated attacker VLAN.

The demonstration does not establish physical actuation of aerators, pumps, or feeders. SAFE/HOLD status should be described as monitoring or control-state logic unless physical control has been separately demonstrated.

## Operation and Verification

1. Start the GNS3 project and verify that `NAT1`, `Switch1`, and the four virtual endpoints are available.
2. Confirm node IP addresses against [network-addressing.md](network-addressing.md).
3. Verify DNS resolution and outbound connectivity to `broker.hivemq.com`.
4. Start the project sensor publishers and the Gateway using the scripts and configuration maintained in the repository.
5. Confirm successful MQTT connection and inspect Gateway logs for accepted and rejected messages.
6. Open the Node-RED monitoring environment on the host PC and verify current readings and alerts.
7. Run only authorised attack demonstrations and preserve the relevant evidence.

Do not clear replay-state files or replace HMAC secrets as a routine troubleshooting step. Reproduction requires the existing project configuration and appropriate key material; no secrets should be committed to GitHub.

## Limitations and Future Work

The demonstrated topology is a single-subnet prototype. It does not implement separate pond networks, firewall-enforced segmentation, broker-side topic ACLs, or a private redundant MQTT service. The working Gateway WebSocket connection on port `8000` is not TLS-encrypted.

Potential future improvements include segmented pond and management networks, MQTT authentication and ACLs, TLS, secure key storage and rotation, broker resilience, calibrated field sensors, and validated physical fail-safe controls.



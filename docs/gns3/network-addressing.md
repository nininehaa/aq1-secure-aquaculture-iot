# AQ-1 GNS3 Network Addressing

## Overview

This document records the IPv4 addressing of the AQ-1 GNS3 demonstration environment. The implemented topology uses one shared network, `192.168.127.0/24`. Proposed multi-subnet designs are not part of this deployment.

## Implemented Addressing

| Node | IPv4 address | Network role |
|---|---|---|
| `Attacker1` | `192.168.127.133/24` | Controlled attack-test endpoint |
| `DO-001` | `192.168.127.138/24` | Simulated dissolved-oxygen publisher |
| `PH-001` | `192.168.127.139/24` | Simulated pH publisher |
| `AQ1-Gateway` | `192.168.127.140/24` | MQTT subscriber and message-verification gateway |
| `Switch1` | No management IP documented | Layer 2 connectivity |
| `NAT1` | Gateway service observed at `192.168.127.2` | Outbound network connectivity |
| `AQ1-Monitor` | Host PC; address not specified here | Node-RED monitoring |
| MQTT broker | `broker.hivemq.com` (external hostname) | Public MQTT messaging service |

**Subnet:** `192.168.127.0/24`  
**Subnet mask:** `255.255.255.0`  
**Observed default gateway for `AQ1-Gateway`:** `192.168.127.2`

The Gateway default route has been checked. The individual default routes of the other virtual endpoints should be verified on their respective hosts when needed. No IP address is assigned here to the physical temperature sensor, the public broker, or the host-PC monitor.

## Network Connectivity

```text
Attacker1  192.168.127.133 ---+
DO-001     192.168.127.138 ---+--- Switch1 --- NAT1 --- Internet
PH-001     192.168.127.139 ---+                     |
AQ1-Gateway 192.168.127.140 --+                     +--- broker.hivemq.com

Host PC / AQ1-Monitor --------------------------------+--- broker.hivemq.com
```

The host PC communicates with the external broker through its own network connection. The diagram represents logical communication and does not assign the monitor to the GNS3 `/24` network.

## MQTT Gateway Connection

| Parameter | Confirmed Gateway value |
|---|---|
| Broker | `broker.hivemq.com` |
| Transport | MQTT over WebSockets |
| TCP port | `8000` |
| WebSocket endpoint | `/mqtt` |
| Subscription | `aquaculture/sensors/#` |

The Gateway received a successful MQTT connection acknowledgement (`CONNACK`, return code `0`). The broker is an external service; no local Mosquitto server is documented as part of this GNS3 deployment.

## Network and Security Boundaries

All four GNS3 endpoints share the same subnet and switch. There is no documented network-layer separation between attacker and sensor nodes in this implementation.

Application-layer security is provided by the AQ-1 Gateway's HMAC-SHA256 verification and replay checks. These checks should not be described as substitutes for TLS, network segmentation, MQTT broker authentication, or topic ACLs.

The Gateway's port `8000` WebSocket connection is not encrypted by TLS. Transport settings for other clients should be confirmed from their respective configurations.

## Proposed Expansion (Not Implemented)

| Proposed segment | Example subnet | Intended purpose |
|---|---|---|
| Pond A | `10.10.10.0/24` | Pond A sensor devices |
| Pond B | `10.10.20.0/24` | Pond B sensor devices |
| Pond C | `10.10.30.0/24` | Pond C sensor devices |
| Management | `10.10.50.0/24` | Administration |
| Monitoring | `10.10.60.0/24` | Monitoring and logging |
| Security/Test | `10.10.70.0/24` | Isolated attack testing |

These addresses are design options only and must not be reported as deployed. A future implementation would also require routing, firewall policies, and corresponding test evidence.

## Configuration Maintenance

When changing the network, update node addresses, default routes, broker settings, and the architecture documentation together. Record any changes based on actual device configuration and connectivity tests. Do not commit credentials, HMAC secrets, or sensitive runtime state.

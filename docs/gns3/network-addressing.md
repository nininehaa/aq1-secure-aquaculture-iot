# Planned GNS3 Network Addressing

## Status

**Planned addressing scheme.**

These addresses are reserved for the proposed GNS3 scale-up. They are not evidence that the full virtual network has already been deployed.

## Purpose

The project will separate sensor, management, monitoring and security/test traffic instead of placing every component on one local network.

Using separate IP networks makes it easier to:

- control which devices can communicate
- create firewall rules
- isolate pond sensor traffic
- separate monitoring and management systems
- place attacker/test devices in a controlled segment
- capture and explain traffic flows during demonstrations

## Proposed Addressing Plan

| Network | Subnet | Purpose |
|---|---|---|
| Pond A | `10.10.10.0/24` | Pond A sensor devices |
| Pond B | `10.10.20.0/24` | Pond B sensor devices |
| Pond C | `10.10.30.0/24` | Pond C sensor devices |
| Management | `10.10.50.0/24` | Administration/configuration |
| Monitoring | `10.10.60.0/24` | Monitoring, logging and security services |
| Security/Test | `10.10.70.0/24` | Attacker/test devices and controlled security testing |

## First Milestone Addressing

The first working GNS3 path only needs a small part of the full plan.

Suggested first layout:

| Component | Example network | Purpose |
|---|---|---|
| `TEMP-001` sensor node | Pond A `10.10.10.0/24` | Generate authenticated HMAC-protected temperature readings |
| Router/firewall | Connects Pond A and service networks | Route and later filter traffic |
| Mosquitto broker node | Service/monitoring side | Receive authenticated MQTT traffic |
| Monitoring node | Monitoring `10.10.60.0/24` | Verify readings and generate alerts |

Exact host addresses will be recorded once the GNS3 nodes are created.

## Traffic That Should Be Allowed

For the first milestone:

```text
TEMP-001 -> Mosquitto : TCP 1883
Monitoring -> Mosquitto : TCP 1883
```

Later, when TLS is added, the project may move MQTT traffic to a TLS-enabled listener such as TCP `8883`.

## Traffic That Should Be Restricted

The final design should avoid giving sensor devices unrestricted access to management or monitoring systems.

Examples of intended controls:

- pond sensors should reach the MQTT service they require
- pond sensors should not have unrestricted access to management systems
- attacker/test network traffic should be restricted by firewall rules
- management traffic should be separated from normal sensor traffic
- MQTT topic ACLs should restrict what each MQTT identity can publish or subscribe to

## Documentation Rule

When actual IP addresses are assigned in GNS3, update this file with:

- node name
- interface
- exact IP address
- subnet mask/prefix
- default gateway
- role
- allowed services

Do not mark planned addresses as implemented until the topology has been tested.

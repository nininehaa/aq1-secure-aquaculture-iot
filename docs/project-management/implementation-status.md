# Implementation Status

**Project:** AQ-1 Secure and Resilient Aquaculture IoT System  
**Client scenario:** Coral Coast Aquaculture  
**Purpose:** Give the team, tutor and reviewers one honest source of truth for what is working, what is only designed, and what still requires evidence.

## Status Definitions

- **Implemented** — working code or configuration exists.
- **Tested / PASS** — implementation has been executed and a recorded test passed.
- **In progress** — implementation work has started but acceptance criteria are not yet complete.
- **Planned** — design exists, but the component has not yet been built and demonstrated.
- **Pending** — required work has not yet started or has no acceptable evidence.

## Current System Status

| Component | Current status | Working evidence | Remaining work |
|---|---|---|---|
| Dissolved-oxygen sensor simulator | Implemented / Tested | `scripts/sensors/do_sensor.py`; Week 6 security tests | Move into the final GNS3 path and capture network evidence |
| Temperature sensor simulator | Implemented / Tested locally | `scripts/sensors/temperature_sensor.py`; temperature HMAC/tamper tests | Move into the final GNS3 path and retest across the virtual network |
| pH sensor simulator | Pending | Project scope/design only | Implement producer, identity, message format and tests |
| Mosquitto MQTT broker | Implemented locally | `configs/mosquitto/mosquitto.conf`; authentication test evidence | Deploy as a GNS3 service node; finish topic ACLs; authenticate monitoring client |
| HMAC-SHA256 message integrity | Implemented / Tested | DO and temperature signing/verification tests | Standardise message format and key handling across all sensor types |
| Security monitoring | Implemented locally / Tested | `scripts/monitoring/monitor.py`; HMAC rejection and outage/recovery tests | Run on a separate GNS3 node and receive MQTT across the virtual network |
| Per-sensor outage/recovery detection | Implemented / Tested | Week 6 tests | Repeat test in GNS3 with one sensor stopped while another remains active |
| SAFE/HOLD controller | Pending integration | `docs/implementation/failsafe-controller.md`; Issue #18 | Build controller, consume trusted/outage state, demonstrate activation and recovery |
| GNS3 routed deployment | In progress | `docs/gns3/gns3-design.md`; `docs/gns3/network-addressing.md`; Issue #16 | Build nodes, addressing, routing/firewall, live MQTT path and packet capture |
| MQTT topic ACLs | In progress | Issue #17; broker security design | Implement and test authorised/unauthorised topic access |
| Attacker/test node | Planned | Threat model and GNS3 design | Add test node and demonstrate rejected credentials/spoof/tamper attempts |
| Packet capture / Wireshark evidence | Pending | Planned test evidence | Capture traffic from the actual GNS3 path and link captures/screenshots to test cases |
| Node-RED/dashboard | Planned | Architecture documentation | Build only after core GNS3 security path and SAFE/HOLD integration are stable |
| TLS | Planned | Security design | Configure and verify later; do not mark implemented until packet capture confirms it |

## Current Working End-to-End Slice

The strongest implemented slice at present is:

`DO / Temperature simulator -> Mosquitto MQTT -> security monitor -> trusted/rejected/outage decision`

This slice currently runs as a local prototype. The next implementation milestone is to reproduce at least one complete sensor-to-monitor path across separate GNS3 nodes.

## Next Acceptance Milestone

The team can mark the first GNS3 milestone **Tested / PASS** only when all of the following are demonstrated:

1. A sensor runs on a separate GNS3 node or endpoint.
2. The sensor reaches Mosquitto across the virtual network using its assigned IP path.
3. Correct MQTT credentials are accepted and incorrect credentials are rejected.
4. A signed reading reaches the monitoring node.
5. The monitoring node validates a correct HMAC and rejects a tampered HMAC.
6. Stopping the sensor causes that specific sensor to enter outage state without another sensor masking the failure.
7. Terminal output, configuration, IP information and packet-capture evidence are committed or linked.

## Evidence Rule

A feature is not complete because code exists. For this project, completion means **built + configured + run + tested + evidenced + documented**.

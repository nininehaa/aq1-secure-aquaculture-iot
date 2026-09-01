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
| Dissolved-oxygen sensor simulator | Implemented / Tested locally | `scripts/sensors/do_sensor.py`; Week 6 security tests | Move into the Pond A GNS3 path and capture network evidence |
| Temperature sensor | Implemented / Tested in GNS3 | `scripts/sensors/temperature_sensor.py`; `docs/gns3/week8-temp-monitor-validation.md` | Retest after broker authentication/ACL hardening and final routed topology are added |
| pH sensor | Pending | Project scope/design only | Implement producer, identity, message format and tests |
| Mosquitto MQTT broker | Implemented in GNS3 / connectivity tested | Separate GNS3 broker node at test address `192.168.42.130`; `docs/gns3/week8-temp-monitor-validation.md` | Restore/enforce broker authentication in GNS3; authenticate monitor; finish topic ACLs; move to final routed topology |
| HMAC-SHA256 message integrity | Implemented / Tested locally and temperature tested in GNS3 | DO and temperature signing/verification tests; GNS3 temperature tamper rejection | Standardise message format/key handling across all sensor types |
| Security monitoring | Implemented / Tested in GNS3 for temperature path | Separate `Neha-Monitor-1` node; `monitor.py`; valid/tamper/outage/recovery GNS3 results | Authenticate monitoring client; add final routed/network and packet-capture evidence; validate DO/pH paths |
| Per-sensor outage/recovery detection | Implemented / Tested in GNS3 for TEMP-001 | TEMP-001 stop -> outage after 10 seconds -> restart -> recovery | Repeat with full Pond A sensor set and verify one sensor cannot mask another |
| SAFE/HOLD controller | Pending integration | `docs/implementation/failsafe-controller.md`; Issue #18 | Build controller, consume trusted/outage state, demonstrate activation and recovery |
| GNS3 Pond A deployment | In progress — first virtualised slice working | Separate TEMP-001, Mosquitto and monitor nodes connected through GNS3 switch; `docs/gns3/week8-temp-monitor-validation.md` | Replace temporary flat switch/NAT path with planned routed Pond A/router-firewall path; add DO/pH; capture traffic |
| MQTT broker authentication in GNS3 | Pending hardening | Local authenticated broker evidence exists; GNS3 test used temporary anonymous listener | Re-enable credentials in GNS3; verify valid credentials accepted and missing/incorrect credentials rejected; authenticate monitor |
| MQTT topic ACLs | In progress | Issue #17; broker security design | Implement and test authorised/unauthorised topic access |
| Attacker/test node | Planned | Threat model and GNS3 design | Add test node if needed and demonstrate rejected credentials/spoof/tamper attempts |
| Packet capture / Wireshark evidence | Pending | Planned test evidence | Capture traffic from the actual GNS3 path and link captures/screenshots to test cases |
| Node-RED/dashboard | Planned | Architecture documentation | Build only after core GNS3 security path and SAFE/HOLD integration are stable |
| TLS | Planned | Security design | Configure and verify later; do not mark implemented until packet capture confirms it |

## Current Working End-to-End Slice

The strongest demonstrated virtualised slice is now:

```text
TEMP-001 GNS3 node
      |
      v
Mosquitto GNS3 broker
      |
      v
Neha-Monitor-1 GNS3 node
      |
      +--> valid HMAC -> ACCEPTED
      +--> sensor stopped -> OUTAGE ALERT
      +--> valid sensor returns -> RECOVERY
      +--> tampered payload -> REJECTED
```

This is the first working GNS3 sensor-to-monitor security slice. It currently uses a temporary flat GNS3 switch/NAT network for integration testing rather than the final routed Pond A/router-firewall design.

## GNS3 Validation Result

The following have been demonstrated for TEMP-001 across separate GNS3 nodes:

1. TEMP-001 publishes through the virtual network to a separate Mosquitto broker.
2. The monitoring node connects to the separate broker on TCP port 1883 and subscribes to project topics.
3. Valid HMAC-protected temperature readings are accepted.
4. A controlled tampered temperature payload is rejected because HMAC verification fails.
5. Stopping TEMP-001 causes an outage alert after the configured 10-second threshold.
6. Restarting TEMP-001 produces a recovery event and valid readings are accepted again.

See `docs/gns3/week8-temp-monitor-validation.md` for the detailed test record.

## Remaining First-MVP Acceptance Work

The first virtualised slice is working, but the full Pond A milestone is **not complete**. Remaining acceptance work includes:

1. Replace the temporary flat switch/NAT integration network with the planned Pond A routed/router-firewall path.
2. Restore and enforce MQTT authentication in the GNS3 broker.
3. Authenticate the monitoring client.
4. Implement and verify topic ACL rules.
5. Add packet-capture/Wireshark evidence.
6. Move/validate DO and implement/validate pH in the Pond A path.
7. Integrate SAFE/HOLD and demonstrate activation/recovery from trusted monitoring state.

## Evidence Rule

A feature is not complete because code exists. For this project, completion means **built + configured + run + tested + evidenced + documented**.

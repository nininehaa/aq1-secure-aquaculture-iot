# Requirements and Traceability Matrix

**Project:** AQ-1 Secure and Resilient Aquaculture IoT System

This matrix links the project requirements to implementation ownership, technical evidence and acceptance tests. It should be updated whenever a requirement changes or new evidence is produced.

| ID | Requirement | Primary owner/workstream | Implementation/evidence | Acceptance evidence | Status |
|---|---|---|---|---|---|
| R-01 | Simulate aquaculture water-quality readings for dissolved oxygen, temperature and pH | Sensor/MQTT workstream | `scripts/sensors/` | Each sensor publishes identifiable readings through the agreed MQTT path | DO/TEMP implemented; pH pending |
| R-02 | Only authorised sensor clients should connect/publish to the MQTT broker | Sensor/MQTT/network security | `configs/mosquitto/`; Issue #17 | Valid credentials accepted; missing/invalid credentials rejected | Partially tested locally |
| R-03 | Sensor messages must include integrity protection so altered data can be detected | Sensor producer + monitoring | HMAC-SHA256 in sensor code and `scripts/monitoring/monitor.py` | Valid message accepted; altered message rejected | Implemented / tested for DO and TEMP |
| R-04 | The monitor must verify data before treating it as trusted | Security monitoring | `scripts/monitoring/monitor.py` | Invalid HMAC does not update trusted sensor state | Implemented / tested |
| R-05 | Availability must be tracked independently per expected sensor | Security monitoring | per-sensor last-valid-message tracking | Stop one sensor while another remains active; only stopped sensor reports outage | Implemented / tested locally |
| R-06 | Recovery must be identified when valid trusted data resumes | Security monitoring | recovery state in monitor | Restart stopped sensor; valid HMAC causes recovery event | Implemented / tested locally |
| R-07 | Missing or untrusted critical sensor data must lead to a safe control response | Control/resilience workstream | Issue #18; `docs/implementation/failsafe-controller.md` | Tamper/outage causes SAFE/HOLD; trusted recovery follows defined transition | Pending |
| R-08 | Components must be deployed across a virtualised network rather than only localhost | Shared GNS3 implementation | Issue #16; `docs/gns3/` | Sensor, broker and monitor communicate across separate GNS3 nodes/endpoints with recorded IPs | In progress |
| R-09 | Network access should be restricted using routing/firewall/ACL controls | Sensor/MQTT/network security | GNS3 design; Issue #17 | Allowed MQTT path works; unauthorised path/topic is blocked and evidenced | Pending implementation |
| R-10 | Security events and sensor health changes must be observable | Security monitoring | monitor logs; planned dashboard | Accepted, rejected, outage and recovery events can be shown during demo | Partially implemented |
| R-11 | The project must retain reproducible implementation documentation | Shared | `docs/`, configuration files, setup guides | Another team member can rebuild/run the documented slice | In progress |
| R-12 | Tests must distinguish malformed data, integrity failure, authentication failure and availability failure | Shared assurance | `testing/` | Each failure has a separate test case, expected result and actual result | Partially implemented |

## Traceability Workflow

For every material change, update the chain below:

`Requirement -> Issue/Kanban task -> implementation commit/PR -> test case -> evidence -> status`

A requirement should not be marked complete until the implementation and its acceptance evidence can both be pointed to.

## Change Control

If scope changes (for example, sensor count, GNS3 topology, security controls or SAFE/HOLD behaviour):

1. Record the reason in `docs/project-decisions.md`.
2. Update this traceability matrix.
3. Update the relevant GitHub issue/owner.
4. Update architecture and implementation-status documentation.
5. Retest any acceptance criteria affected by the change.

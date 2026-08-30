# Project Risk Register

**Project:** AQ-1 Secure and Resilient Aquaculture IoT System

Use this as a live register. Review it at least weekly and whenever a major implementation decision changes risk exposure.

| ID | Risk | Likelihood | Impact | Current mitigation / control | Owner/workstream | Status |
|---|---|---|---|---|---|---|
| RK-01 | Project remains a localhost code demo rather than a virtualised implementation | High | High | Build first sensor -> GNS3 network -> broker -> monitoring slice; capture IP and packet evidence | Shared / GNS3 | Open |
| RK-02 | GNS3 setup consumes too much time and delays core MVP | Medium | High | Start with one thin end-to-end sensor path before multi-pond/multi-node expansion | Shared / GNS3 | Open |
| RK-03 | One active sensor masks another sensor outage | Low after control | High | Maintain per-sensor last-valid-message state; test one-sensor outage while another remains active | Monitoring | Controlled locally; retest in GNS3 |
| RK-04 | Forged or tampered MQTT messages are treated as trusted | Low after control | High | HMAC-SHA256 verification; reject mismatch before updating trusted state | Monitoring + sensor producer | Controlled for DO/TEMP locally |
| RK-05 | Invalid traffic keeps a failed sensor marked healthy | Low after control | High | Update availability timestamp only after successful integrity verification | Monitoring | Controlled locally |
| RK-06 | Unauthorised MQTT clients can connect or publish | Medium | High | Username/password authentication now; finish topic ACLs; later strengthen with TLS/certificate controls if in scope | MQTT/network security | Partially controlled |
| RK-07 | Credentials or HMAC secrets are committed to GitHub | Medium | High | Use environment variables/local password files; `.gitignore`; review commits before push | All | Active control |
| RK-08 | SAFE/HOLD remains documentation-only and cannot be demonstrated | High | High | Implement minimal controller state machine early; define exact trusted/outage input contract and acceptance test | Control/resilience | Open |
| RK-09 | Documentation claims planned features are complete | Medium | Medium | Use status labels: Implemented, Tested/PASS, In progress, Planned, Pending; maintain `implementation-status.md` | All / PM | Active control |
| RK-10 | Team contributions become difficult to attribute | Medium | High | One owner per issue/card; member-specific branches/commits; avoid writing another member's individual progress evidence | All / PM | Active control |
| RK-11 | Inconsistent MQTT payload/topic formats break integration | Medium | Medium | Define canonical payload fields/topics; document interface; add integration test before GNS3 expansion | Shared integration | Open |
| RK-12 | pH sensor remains unimplemented while architecture presents three completed sensors | Medium | Medium | Clearly mark pH pending until code and test evidence exist; schedule implementation task | Sensor workstream | Open |
| RK-13 | Demo fails because setup is not reproducible | Medium | High | Maintain setup/runbook, required environment variables, start order, expected output and recovery steps | All | Open |
| RK-14 | Network/security controls cannot be proven to tutor | Medium | High | Capture GNS3 topology, configuration snippets, test logs and Wireshark evidence for each acceptance test | Shared assurance | Open |

## Rating Guidance

- **Likelihood:** Low / Medium / High based on current project conditions.
- **Impact:** Low / Medium / High based on effect on safety objective, assessment evidence, schedule or demo.

## Weekly Risk Review

At each team review:

1. Check whether likelihood or impact changed.
2. Record newly discovered risks.
3. Close a risk only when evidence shows the control works.
4. Convert important mitigation work into a GitHub issue with an owner.
5. Link implementation/test evidence when a risk is reduced.

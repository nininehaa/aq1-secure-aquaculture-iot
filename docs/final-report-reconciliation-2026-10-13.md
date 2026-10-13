# AQ-1 final report ↔ repository reconciliation

**Reviewed:** 13 October 2026  
**Baseline:** submitted `Group-6_AQ1_Final_Report_All.pdf` (53 pages)  
**Repository main revision examined:** `23caeb553224eb6c1e212d144f608d3333c9036f`

This checklist records *what is and is not in the GitHub repository*. It does **not** replace the submitted report or claim missing assets/tests exist.

## 1. As-submitted prototype (from Technical Artefact 2)

- One **physical ESP32-C3 + waterproof DS18B20** temperature source, published over Wi-Fi.
- **DO-001 and PH-001 simulated** sensor publishers in GNS3 / Alpine Docker nodes, hosted using VMware.
- **Public HiveMQ MQTT** broker `broker.hivemq.com:1883` used during the final showcase. This connection is **not TLS-protected**. Local Mosquitto was used during earlier development.
- A **Python GNS3 verification gateway** checks message HMAC; replay-sequence checks are reported, with timestamp freshness checks for simulated DO/pH (but *not* comparable Unix timestamp freshness for the ESP32's uptime timestamp).
- **Node-RED + SQLite** provide the dashboard and event/monitoring storage.
- **NORMAL / SAFE-HOLD is software indication only**: no physical pumps, aerators, feeders or relays were actuated.
- Recorded screenshots support valid-reading acceptance, DO replay rejection and outage/software-safe-state indication. Do **not** call the replay screenshot a wrong-HMAC screenshot.
- The report does **not** establish successful external/cross-team attacker testing, complete hardware actuation, TLS or topic ACL enforcement.

## 2. Repository inventory versus final showcase

| Item | Repo status as reviewed | Action |
| --- | --- | --- |
| Earlier Python DO and temperature publishers | Present in `scripts/sensors/` | Keep and label *historical*; do not claim they are final GNS3 exporters |
| Earlier MQTT gateway | Present in `scripts/gateway/gateway.py` | Mark as *historical*. It uses `localhost`, earlier topic format and a hard-coded sample key; **not** the final HiveMQ gateway |
| Earlier monitoring and security scripts | Present under `scripts/monitoring/` and `scripts/security/` | Retain as earlier tests; do not silently substitute for final attacker scripts |
| Final GNS3 project export | **Not found in repository tree** | Obtain actual `.gns3project`/portable export from teammate; sanitise; upload with setup details |
| Final GNS3 gateway and DO/PH scripts | **Not found as clearly identified final copies** | Export actual tested scripts from nodes, preserving versions and message formats |
| Final attack scripts (spoof/tamper/replay) | **Not found as clearly identified final copies** | Export actual attacker-node `demo.py`/capture/replay scripts and redacted output |
| ESP32-C3 Arduino firmware `*.ino` | **Not found** | Add actual compiled/uploaded sketch, wiring diagram and safe config example; remove Wi-Fi passwords and signing keys |
| Final Node-RED `flows.json`, dashboard config | **Not found** | Export actual Node-RED flows and redact credentials, tokens and private addresses |
| SQLite monitoring schema / reproducible setup | **Not found as final showcase package** | Add schema or sanitised sample database plus import instructions; do not commit unredacted live data |
| Security test captures | Week-7 images and early plans are present; final screenshots from report are not fully mapped to versioned files | Add per-test attack input, gateway response, timestamp, expected/observed result; link to report figure |
| Azure dashboard experiment | Present in `azure-dashboard/` | Clearly label **experimental, not final showcase**; avoid implying its deployment worked |
| Demo setup guidance | `docs/setup/local-demo-setup.md` describes **earlier local Mosquitto** only | Keep as historical, create separate final GNS3 runbook from actual export |
| Documentation, AI log, risk register | Present | Keep history intact; ensure final files are separately indexed |

## 3. Specific inconsistencies and security concerns

1. **Final vs early gateway:** The root README correctly describes the physical/GNS3 + HiveMQ system, but linking the old `scripts/gateway/gateway.py` as though it were the showcase gateway would be misleading. Final as-built gateway must be supplied separately.
2. **Public broker:** HiveMQ port 1883 is public and unencrypted, with no proven topic ACLs/broker authentication in the final demonstration. HMAC provides message integrity/authenticity for key holders, *not* confidentiality or broker access control.
3. **Development secret:** `scripts/gateway/gateway.py` contains `SECRET_KEY = b"aq1-week5-secret-key"`. Treat this as an **exposed development key**, never reuse it for any real device or public broker. Move samples to environment variables in a tested follow-up change; rotate any key actually used elsewhere. Removing it in a new commit does not erase Git history.
4. **Mosquitto config:** `configs/mosquitto/mosquitto.conf` uses a local Windows DLL/path; it is **not** a portable deployment configuration or evidence of final HiveMQ authentication.
5. **ESP32 replay freshness:** Report states the firmware sends uptime-based timestamps. Sequence protection is reported, but Unix-age validation cannot honestly be claimed for the physical sensor.
6. **Control outputs:** SAFE/HOLD in the report is a displayed supervisory state, not physical pump/relay control.
7. **Evidence precision:** Report Figure 11 documents **DO replay rejection**, while distinct proof of wrong-HMAC rejection is still called for in its implementation evidence register.
8. **Report artefact naming:** Early report summary contains pending file names and references a separate `AQ1_setup.zip`. Verify this is actually available to markers and ensure repository links to the true final handover rather than fabricated file names.

## 4. Preferred repository organisation (only after actual files are recovered)

```text
final-showcase/
  README.md                  # verified host prerequisites + run sequence
  gns3/                      # sanitised exported final GNS3 project
  gateway/                   # actual final verified gateway source
  sensors/                   # actual DO-001 and PH-001 scripts
  attacker/                  # actual spoof/tamper/replay demo scripts
  esp32/                     # actual ESP32-C3 .ino + wiring + config example
  node-red/                  # sanitised exported flows + dependencies
  sqlite/                    # schema + safe sample data
  evidence/                  # dated/redacted terminal, dashboard and attack captures
```

**Do not upload placeholder files and label them implemented.** Include a manifest with file hash or source revision, date of capture, which teammate supplied each asset, exact commands used in the final showcase, and known limitations.

## 5. Minimal repeatable verification to collect

| Case | Input/action | Required observed evidence |
| --- | --- | --- |
| Normal | Publish valid DO and physical TEMP messages | Gateway ACCEPTED + Node-RED trusted updates |
| Spoof | Forged DO sensor ID with invalid HMAC | Gateway rejects, dashboard trusted reading unchanged |
| Tamper | Change signed value but retain old HMAC | HMAC mismatch rejection captured separately |
| Replay | Replay *previously valid* DO message with old sequence | Sequence rejection log (matches report Figure 11) |
| Outage | Stop a trusted source for configured watchdog time | Offline alert, software SAFE/HOLD displayed; no claim of pump action |
| Recovery | Resume signed newer messages | Only claim automatic recovery if a repeatable log proves it |

Perform attacks **only against authorised AQ-1 test subjects**; do not probe unrelated users of the shared public broker. Confirm secret redaction before any upload.

## 6. Contribution / traceability

The submitted report attributes contributions to **Neha, Sahil and Arnob** and gives a nominal 33.33/33.33/33.34 percent split, while also asking the team to confirm the final technical lead scope. Preserve the real commit history, assign each missing asset to its actual owner, and link the upload/PR to its source. Do not rewrite authorship simply to make allocations look balanced.

## 7. What this reconciliation branch changes

Documentation **only**. No executable code, MQTT settings, keys, demo scripts or existing historical documents have been altered. The next step is to retrieve the real final showcase package from the teammates and compare its runtime code to the report before making functional modifications.

# AI Use Log

## 2026-08-04 — Initial project planning

- Tool: ChatGPT
- Used by: Neha Thanait and Sahil Basnet
- Purpose: Understanding the AQ-1 project and organising the initial project setup.
- Prompt summary: Requested step-by-step help to understand and begin the project.
- Output used: Project explanation, GitHub setup instructions and proposed initial structure.
- Changes made by the team: The team reviewed and adapted suggestions to match the approved AQ-1 scenario.
- Validation: Information was compared with the AQ-1 scenario, Capstone Checklist, Weekly Guide and Teamwork Framework.

## 11 August 2026 — Week 5 Technical Development

### Sahil Basnet

**Tool:** ChatGPT

**Purpose:** Used as a technical support resource while setting up the MQTT prototype and troubleshooting the initial sensor-to-gateway communication.

**AI-assisted areas:**
- MQTT/Mosquitto setup guidance
- Python MQTT publishing and subscribing examples
- troubleshooting installation and connection issues

**Student contribution and validation:** Sahil installed and configured the required software, created and ran the dissolved-oxygen sensor and gateway scripts, tested MQTT publish/subscribe behaviour, resolved local setup issues, and verified the sensor-to-gateway workflow before committing the implementation to GitHub.

### Neha Thanait

**Tool:** ChatGPT

**Purpose:** Used as a consultation and troubleshooting resource while developing the monitoring and testing component of the prototype.

**AI-assisted areas:**
- MQTT monitoring structure
- timestamped event logging
- timeout-based sensor outage detection
- initial acceptance-test planning

**Student contribution and validation:** Neha configured and ran the monitoring environment, tested incoming dissolved-oxygen readings, verified that readings were written to the log, implemented and tested the sensor timeout behaviour, and manually stopped the sensor to confirm that the system generated an outage alert after the configured 10-second threshold. The monitoring and test artefacts were reviewed and committed through Neha's GitHub branch before being merged into main.

## 17–18 August 2026 — Week 6 Security Integration and Testing

### Neha Thanait

**Tool:** ChatGPT

**Purpose:** Used for troubleshooting support, security-test planning and documentation refinement while extending the monitoring component.

**AI-assisted areas:**
- per-sensor outage/recovery logic review
- HMAC verification troubleshooting
- controlled tamper-test planning
- interpreting malformed-message versus HMAC-failure results
- structuring Week 6 security/acceptance-test evidence

**Student contribution and validation:** Neha ran the monitor and sensor/test scripts, verified valid temperature readings, stopped the sensor to confirm outage detection, ran a controlled tamper test, confirmed HMAC rejection, restarted the legitimate sensor and confirmed recovery. AI suggestions were only retained where the behaviour could be reproduced in the local environment and supported by GitHub/test evidence.

## 30 August–1 September 2026 — Repository Documentation and Scope Clarification

### Neha Thanait

**Tool:** ChatGPT

**Purpose:** Used to review the existing repository structure, identify confusing or stale documentation, and help organise the project plan so the team has one clear view of the MVP, ownership and remaining work.

**AI-assisted areas:**
- reviewing documentation structure and duplicated/stale status information
- separating the one-Pond-A MVP from later multi-pond/stretch architecture
- organising the project plan, implementation-status, traceability and risk documentation
- identifying stale issue wording
- improving documentation navigation and consistency

**Student contribution and validation:** The repository content, existing proposal direction, Week 6 progress records, current issues and implementation evidence were reviewed before changes were made. The project plan was clarified so it does not claim that Pond B/Pond C, backup broker, TLS or other stretch items are already required or complete. Existing technical evidence was not replaced by AI-generated claims.

## Ongoing AI-use rule

Each team member should record their own meaningful AI use when it contributes to planning, troubleshooting, code/configuration support, testing or documentation. A team member's AI use should not be recorded on their behalf unless confirmed.

AI-generated suggestions are not implementation evidence by themselves. Technical outputs must be understood, tested and validated by the student/team before being treated as project evidence. The team remains responsible for all submitted code, configuration, tests and documentation.

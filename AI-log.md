# AI Use Log

## 2026-08-04 — Initial project planning

- Tool: ChatGPT
- Used by: Neha Thanait and Sahil Basnet
- Purpose: Understanding the AQ-1 project and organising the initial project setup.
- Prompt summary: Requested step-by-step help to understand and begin the project.
- Output used: Project explanation, GitHub setup instructions and proposed initial structure.
- Changes made by the team: The team will review and adapt all suggestions to match the approved AQ-1 scenario.
- Validation: Information was compared with the AQ-1 scenario, Capstone Checklist, Weekly Guide and Teamwork Framework.

## 11 August 2026 – Week 5 Technical Development

### Sahil Basnet

**Tool:** ChatGPT

**Purpose:**  
Used as a technical support resource while setting up the MQTT prototype and troubleshooting the initial sensor-to-gateway communication.

**AI-assisted areas:**  
- MQTT/Mosquitto setup guidance
- Python MQTT publishing and subscribing examples
- Troubleshooting installation and connection issues

**Student contribution and validation:**  
Sahil installed and configured the required software, created and ran the dissolved-oxygen sensor and gateway scripts, tested MQTT publish/subscribe behaviour, resolved local setup issues, and verified the sensor-to-gateway workflow before committing the implementation to GitHub.

---

### Neha Thanait

**Tool:** ChatGPT

**Purpose:**  
Used as a consultation and troubleshooting resource while developing the monitoring and testing component of the prototype.

**AI-assisted areas:**  
- MQTT monitoring structure
- Timestamped event logging
- Timeout-based sensor outage detection
- Initial acceptance-test planning

**Student contribution and validation:**  
Neha configured and ran the monitoring environment, tested incoming dissolved-oxygen readings, verified that readings were written to the log, implemented and tested the sensor timeout behaviour, and manually stopped the sensor to confirm that the system generated an outage alert after the configured 10-second threshold. The monitoring and test artefacts were reviewed and committed through Neha's GitHub branch before being merged into main.

---

## 18–20 August 2026 – Week 6 Sahil Security Integration

### Sahil Basnet

**Tool:** ChatGPT

**Purpose:**  
Used as a technical support and explanation resource while strengthening the temperature-sensor MQTT security implementation, troubleshooting the local demo environment, and improving project documentation.

**AI-assisted areas:**  
- Mosquitto username/password authentication configuration and troubleshooting
- environment-variable handling for MQTT credentials and HMAC secret
- HMAC-SHA256 signing structure for the temperature producer
- controlled temperature tamper-test design
- explanation of authentication versus message integrity
- demo-terminal setup and troubleshooting
- documentation structure for the implemented security controls
- planning the next GNS3 network scale-up

**Student contribution and validation:**  
Sahil ran the temperature sensor and Mosquitto environment locally, configured the required environment variables, verified successful authenticated publishing, used an authorised subscriber to confirm live temperature messages were received, and manually tested a connection without credentials to confirm that Mosquitto rejected unauthorised access. Sahil also reviewed the HMAC output and tamper-test behaviour and committed the temperature producer/security test changes to GitHub.

The following implementation commits provide technical evidence of this work:

- `9a5216d` — authenticated temperature sensor MQTT flow
- `e98556c` — HMAC protection and temperature tamper test
- `fa4ac7c` — HMAC integrity protection in the temperature sensor

Project documentation was then updated to record the implemented controls, known integration gaps and planned GNS3 scale-up.

---

### Validation

AI-generated suggestions were not accepted as evidence by themselves. Technical outputs were tested in the local project environment and adjusted where required. The team remains responsible for understanding, explaining and validating all submitted code, configuration and documentation.

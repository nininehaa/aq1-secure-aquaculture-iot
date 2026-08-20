# Project Decision Log

This file records important technical decisions so the team can explain not only what was chosen, but why it was chosen.

## D01 — Use simulated sensors first

**Decision:** Use Python sensor simulators before moving to physical IoT hardware.

**Reason:** The project needs repeatable security testing. Simulated sensors allow the team to control values, stop sensors deliberately, generate tampered messages, and reproduce tests without depending on physical hardware.

**Current result:** Dissolved-oxygen and temperature sensor simulators are part of the prototype.

## D02 — Use MQTT for sensor messaging

**Decision:** Use MQTT as the communication protocol between sensors and the monitoring/control system.

**Reason:** MQTT fits the publish/subscribe pattern used by IoT systems and lets sensors publish readings to named topics while monitoring components subscribe to the data they need.

**Current result:** The temperature sensor publishes to `aq1/pond1/temperature` through Mosquitto.

## D03 — Use Eclipse Mosquitto as the MQTT broker

**Decision:** Use Eclipse Mosquitto as the MQTT broker.

**Reason:** Mosquitto provides a practical broker for the prototype and supports authentication and later access-control/TLS work.

**Current result:** The broker is running on TCP port `1883`, anonymous access is disabled in the secure configuration, and authorised/unauthorised connection behaviour has been tested.

## D04 — Add MQTT username/password authentication

**Decision:** Require MQTT clients to authenticate to the broker.

**Reason:** A sensor-control system should not allow any anonymous device to connect and publish/subscribe without identity checks.

**Current result:** `TEMP-001` can use valid credentials successfully. A client with no credentials is rejected with `Connection Refused: not authorised`.

## D05 — Use HMAC-SHA256 for message integrity

**Decision:** Add HMAC-SHA256 protection to sensor messages.

**Reason:** MQTT authentication controls who can connect, but does not by itself prove that a received sensor message has not been modified. HMAC gives the monitor a way to verify message integrity using a shared secret.

**Current result:** DO and temperature paths have HMAC verification. The temperature producer signs the canonical field sequence:

`sensor_id|pond_id|sensor_type|value|unit|status|timestamp`

## D06 — Keep secrets out of GitHub

**Decision:** Store MQTT passwords and the temperature HMAC key outside committed source code.

**Reason:** Secrets should not be exposed in the repository.

**Current result:** The temperature sensor reads `AQ1_MQTT_USERNAME`, `AQ1_MQTT_PASSWORD` and `AQ1_TEMP_HMAC_KEY` from environment variables. The local Mosquitto password file is excluded through `.gitignore`.

## D07 — Create controlled tamper tests

**Decision:** Use a separate tamper-test script instead of changing the normal sensor script during security testing.

**Reason:** A separate test is repeatable and clearly separates legitimate behaviour from deliberate malicious test traffic.

**Current result:** `scripts/security/temperature_tamper_test.py` signs an original reading and then changes the value/status after signing so the verifier should reject it.

## D08 — Detect sensor outages independently

**Decision:** Track the last valid reading for each expected sensor.

**Reason:** Continuous sensor data is safety-relevant. A silent or failed sensor should not be treated as healthy just because other sensors are still publishing.

**Current result:** Monitoring detects independent DO and temperature outages and records recovery when valid readings return.

## D09 — Add SAFE/HOLD rather than trusting unreliable data

**Decision:** The final controller should enter a safe state when required trusted sensor data is invalid or unavailable.

**Reason:** The project is not only about detecting attacks. It must also prevent untrusted data from causing unsafe automatic actions.

**Current status:** This control integration is still pending implementation/testing.

## D10 — Scale the project using GNS3

**Decision:** Move from a mainly localhost prototype to a routed and segmented virtual network in GNS3.

**Reason:** The initial prototype proves the security functions but does not represent a realistic multi-network aquaculture deployment. GNS3 allows the team to separate pond networks, broker services, monitoring, management and an attacker/test network and then test routing, firewall rules and packet flows.

**First target:**

```text
TEMP-001 -> Pond A network -> Router/Firewall -> Mosquitto -> Monitoring
```

**Current status:** Architecture and IP planning are documented. Practical GNS3 deployment is the next stage.

# Week 6 Project Progress

## Focus

Week 6 focused on turning the basic MQTT prototype into a more security-focused system and preparing the project for a larger networked deployment.

## Work Completed

### Temperature sensor security

The temperature sensor `TEMP-001` was upgraded to use authenticated MQTT communication.

The sensor now:

- generates simulated temperature readings
- publishes through Mosquitto
- uses MQTT credentials from environment variables
- generates an HMAC-SHA256 value for each protected message
- publishes the sensor ID, pond ID, value, unit, status, timestamp and HMAC

### MQTT authentication testing

The broker configuration disables anonymous access.

Testing confirmed:

- a client with valid credentials can connect and receive live temperature data
- a client with no credentials is rejected with `Connection Refused: not authorised`

### Temperature tamper test

A separate tamper-test script was created.

The test signs an original temperature message and then changes the value and status after signing while keeping the old HMAC.

This produces repeatable modified traffic for the monitoring component to reject.

### Monitoring and integrity verification

The monitoring component was extended so both dissolved-oxygen and temperature messages can be checked for HMAC integrity.

The monitor also tracks outages and recovery independently for the expected sensors.

Only valid readings update the sensor's last-seen time.

### Security testing

The Week 6 test plan now records passing results for:

- valid and invalid DO HMAC
- malformed DO message rejection
- DO outage and recovery
- temperature outage and recovery
- valid temperature HMAC
- tampered temperature rejection
- MQTT rejection of a client with missing credentials

The `SAFE/HOLD` fail-safe activation test remains pending.

### Threat modelling and documentation

Security threats, current controls, implementation status and known limitations were documented so the project is not represented only by code.

### Scale-up direction

The team received feedback that the project needed a larger and more realistic implementation scale.

The response is to use the current working localhost prototype as the baseline for a GNS3 deployment rather than replacing it.

The first GNS3 target is:

```text
TEMP-001
   |
Pond A network
   |
Router / Firewall
   |
Mosquitto broker
   |
Monitoring node
```

Later expansion will add additional pond networks, attacker/test network, access-control rules, backup broker, Node-RED/control and `SAFE/HOLD` integration.

## Known Issues / Remaining Work

- monitoring client still needs MQTT credentials for the authenticated broker
- temperature topic naming needs to be standardised
- topic-level ACL rules need to be added
- TLS is still planned
- `SAFE/HOLD` controller is not yet complete
- GNS3 deployment is planned but not yet demonstrated end-to-end

## Week 6 Outcome

By the end of Week 6 the project had moved beyond a basic MQTT demo.

The prototype now demonstrates sensor simulation, authenticated broker access, message-integrity protection, controlled tampering, HMAC verification, sensor availability monitoring and documented security tests.

The next phase is to integrate the control response and move the same working components into a segmented GNS3 network.

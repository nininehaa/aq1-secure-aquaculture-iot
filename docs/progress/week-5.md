# Week 5 Project Progress

## Focus

Week 5 focused on moving from project planning into a working end-to-end prototype that could produce sensor data, send it through MQTT, monitor it, and begin testing security/availability behaviour.

## Work Completed

### Basic sensor-to-MQTT path

The team created the first working sensor/gateway communication path using Python and Mosquitto MQTT.

The dissolved-oxygen sensor was used as an early working sensor source.

### Monitoring

A monitoring component was added to receive MQTT messages and record sensor events.

### Outage detection

A timeout-based outage mechanism was added so the system could detect when a sensor stopped sending readings.

The sensor was deliberately stopped during testing to confirm the timeout behaviour.

### Initial security work

HMAC-based message integrity was investigated and implemented as a proof of concept, then integrated into the MQTT sensor/security path for dissolved-oxygen readings.

### Test planning

A Week 5 test plan was added to document the first acceptance checks rather than relying only on screenshots or verbal demonstration.

## Problems / Lessons

The Week 5 prototype showed that simply getting MQTT messages from one program to another was not enough for the capstone.

The team needed to make security decisions explicit:

- who is allowed to connect
- whether a message was altered
- whether a sensor is still available
- what the control system should do when data is not trustworthy

This led directly to the stronger Week 6 focus on MQTT authentication, temperature HMAC verification, tamper tests, independent outage tracking and fail-safe planning.

## Evidence in Repository

Important Week 5 repository history includes work such as:

- initial architecture and project overview
- basic MQTT sensor/gateway implementation
- monitoring and Week 5 test plan
- sensor outage detection
- HMAC proof of concept and gateway integration

## Next Step from Week 5

The next development stage was to add a second sensor path, strengthen authentication and integrity controls, and create repeatable negative security tests.

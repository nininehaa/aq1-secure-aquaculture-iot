# Current Week 6 Architecture and Scale-Up Direction

## Current implemented architecture

The Week 6 prototype currently combines simulated aquaculture sensors, MQTT messaging, message-integrity verification and sensor availability monitoring.

```text
Dissolved Oxygen sensor --------------------+
                                             |
Temperature sensor TEMP-001                 |
  - MQTT authentication                     |
  - HMAC-SHA256 generation                  |
  - timestamp/status                        |
              |                              |
              +-------------+----------------+
                            |
                            v
                  Mosquitto MQTT broker
                        TCP 1883
                  anonymous access disabled
                            |
              +-------------+----------------+
              |                              |
              v                              v
     authorised subscriber          monitoring component
                                    - DO HMAC verification
                                    - temperature HMAC verification
                                    - tamper rejection
                                    - outage detection
                                    - recovery detection
                                              |
                                              v
                                      SAFE/HOLD integration
                                           pending
```

## Current security layers

### Device/client access

Mosquitto authentication is enabled for the temperature-sensor path. Missing credentials are rejected by the broker.

### Message integrity

Both dissolved-oxygen and temperature messages have HMAC-based integrity logic in the current repository. The temperature producer uses HMAC-SHA256 over a canonical string containing sensor identity, pond identity, sensor type, value, unit, status and timestamp.

### Availability monitoring

The monitoring component tracks the last valid message for expected sensors and raises an outage alert when valid data is unavailable for more than the configured timeout.

### Fail-safe control

`SAFE/HOLD` remains a control-layer integration task. The intended behaviour is that invalid or unavailable trusted sensor data must not cause harmful automatic control actions.

## Known integration gap

The monitoring client currently calls the MQTT broker without supplying broker credentials. The monitor therefore needs authentication support before the full monitoring path can run against the authenticated broker configuration as one integrated secure system.

## High-scale GNS3 target

The current localhost prototype is the baseline for the next network scale-up.

```text
Pond A IoT network       Pond B IoT network       Pond C IoT network
       |                        |                         |
  sensor nodes             sensor nodes              sensor nodes
       |                        |                         |
  edge gateway             edge gateway              edge gateway
       \                        |                        /
        +-----------------------+-----------------------+
                                |
                         farm router/firewall
                                |
                 +--------------+--------------+
                 |                             |
           MQTT primary                   MQTT backup
                 |                             |
                 +--------------+--------------+
                                |
                    monitoring/security layer
                                |
                         SAFE/HOLD control
                                |
                         Node-RED/dashboard

Separate attacker/test network -> firewall/router -> controlled security tests
```

## Planned network segmentation

Initial proposed segments are:

- Pond A IoT: `10.10.10.0/24`
- Pond B IoT: `10.10.20.0/24`
- Pond C IoT: `10.10.30.0/24`
- Management: `10.10.50.0/24`
- Monitoring: `10.10.60.0/24`
- Security/test network: `10.10.70.0/24`

These addresses are planning values and are not yet claimed as deployed.

## First GNS3 milestone

The first practical GNS3 milestone will move the existing working temperature path away from a single localhost environment:

```text
TEMP-001 node
    |
Pond A virtual network
    |
router/firewall
    |
Mosquitto node
    |
monitoring node
```

Success criteria:

1. `TEMP-001` reaches Mosquitto across a routed GNS3 network.
2. correct MQTT credentials are accepted.
3. missing/incorrect credentials are rejected.
4. HMAC-protected readings arrive unchanged.
5. packet capture shows the actual network path.
6. later security rules restrict unnecessary network access between segments.

## Later resilience tests

After the first routed path is stable, the architecture can be expanded with:

- multiple pond networks
- additional simulated sensor identities
- attacker/test node
- firewall and topic-access rules
- primary and backup MQTT brokers
- broker outage/recovery testing
- Wireshark packet capture evidence
- Node-RED dashboard/control integration
- SAFE/HOLD activation on untrusted or unavailable sensor data

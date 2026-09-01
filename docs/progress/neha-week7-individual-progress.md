# Neha Thanait — Week 7 Individual Technical Progress

## Individual role

**Technical workstream:** Security Monitoring, Trust Validation and Security Testing

My responsibility is to make sure sensor data is checked before the system trusts it. My work focuses on verifying HMAC-protected sensor messages, rejecting tampered or malformed data, detecting sensor outages and recovery, logging security events, and proving these behaviours through tests.

## Important ownership clarification

During Week 7 I built my **own GNS3 validation environment** so I could independently deploy and test my monitoring and trust-validation component.

My GNS3 environment included temporary support nodes for a temperature producer and Mosquitto broker because my monitor needed a live sensor source and broker in order to be tested properly. These support nodes were used to validate my monitoring work and do **not** mean that I am taking ownership of Sahil's final sensor/broker/network-security workstream.

The final group implementation is intended to integrate the three individual technical workstreams:

```text
Sahil: secured sensor / MQTT / network path
                 |
                 v
Neha: monitoring / trust validation / security testing
                 |
                 v
Arnob: SAFE/HOLD / control resilience
```

Each member is expected to build and demonstrate their own technical component, then the team will integrate the components into the final Pond A GNS3 system.

## What I personally worked on in Week 7

During Week 7 I moved my monitoring and trust-validation work from the local prototype into my own GNS3 environment and tested it across separate virtual nodes.

### 1. Built my separate GNS3 monitoring node

I created and configured:

`Neha-Monitor-1`

as an Alpine Linux Docker node in GNS3.

I installed and configured:

- Python 3
- Python virtual environment
- `paho-mqtt`
- the project `monitor.py`

I validated that `monitor.py` compiled without a Python syntax error and confirmed that the MQTT Python library loaded successfully.

### 2. Built temporary support nodes for my validation environment

To test my monitoring component independently, I also created temporary support nodes in the same GNS3 project:

- `AQ1-TEMP-001-1` — test temperature producer
- `AQ1-Mosquitto-Broker-1` — test MQTT broker
- `Switch1` and `NAT3` — temporary connectivity/setup support

These nodes allowed me to generate real MQTT traffic and security events for my monitoring component.

They are not presented as the completed final team topology. Sahil's network/broker-security workstream will later provide the secured broker, routing/segmentation, authentication and ACL controls for the integrated system.

### 3. Connected my monitor to the separate GNS3 Mosquitto broker

The monitor was changed from using only `localhost` to using the broker address supplied through the `AQ1_MQTT_BROKER` environment variable.

The monitor successfully connected to the separate broker node at:

`192.168.42.130:1883`

and subscribed to:

- `aquaculture/sensors/#`
- `aq1/pond1/#`

This proved that my monitoring component could operate from its own GNS3 Linux node rather than only from the original local Windows environment.

### 4. Verified valid temperature HMAC messages across GNS3

The temporary `AQ1-TEMP-001-1` support node published HMAC-protected temperature readings through the test Mosquitto broker.

My monitor received the messages and accepted them only after successful HMAC verification.

Observed result:

`ACCEPTED | Sensor: TEMP-001 | Type: temperature | ... | HMAC: VALID`

**Result: PASS**

### 5. Tested temperature sensor outage detection across GNS3

I stopped the running temperature producer while keeping my monitoring node active.

After more than the configured 10-second timeout, my monitor reported:

`OUTAGE ALERT | Temperature sensor TEMP-001 unavailable | No valid reading for more than 10 seconds`

This confirmed that the per-sensor outage logic still worked when the sensor and monitor were running on separate GNS3 nodes.

**Result: PASS**

### 6. Tested recovery detection across GNS3

I restarted the temperature producer after the outage.

My monitor reported:

`RECOVERY | Temperature sensor TEMP-001 is online again`

and then resumed accepting valid signed readings.

**Result: PASS**

### 7. Tested tampered temperature rejection across GNS3

I used the controlled temperature tamper-test flow. The test created a valid HMAC for an original temperature reading, then modified the temperature value and status without recalculating the HMAC.

The modified payload travelled through the GNS3 MQTT broker, but my monitor rejected it because the received HMAC did not match the modified message contents.

Observed result:

`SECURITY ALERT | Temperature reading rejected | Sensor: TEMP-001 | Reason: HMAC verification failed`

**Result: PASS**

The invalid message did not reset the sensor health timer. This is intentional because invalid or forged data should not make a failed sensor appear healthy.

## My Week 7 GNS3 validation environment

```text
AQ1-TEMP-001-1          temporary test producer
      |
      v
AQ1-Mosquitto-Broker-1  temporary test broker
      |
      v
Neha-Monitor-1          my main technical component
      |
      +--> valid signed reading -> ACCEPTED
      +--> tampered reading -> REJECTED
      +--> no valid reading > 10 seconds -> OUTAGE ALERT
      +--> valid reading returns -> RECOVERY
```

The purpose of this environment was to independently prove my monitoring/security component before final team integration.

## Evidence of my individual work

### Main implementation files

- `scripts/monitoring/monitor.py`
- `docs/implementation/monitoring.md`
- `docs/gns3/week7-temp-monitor-validation.md`

### Earlier individual GitHub evidence

- PR #3 — monitoring and outage-detection work
- PR #14 — per-sensor outage and recovery
- PR #15 — DO HMAC verification and tamper rejection
- Week 5 and Week 6 monitoring/security-test evidence

### Week 7 runtime evidence

Screenshots were captured showing:

- my `Neha-Monitor-1` node running in GNS3
- `monitor.py` present and passing syntax validation
- successful monitor-to-broker connection
- valid `TEMP-001` readings accepted with `HMAC: VALID`
- temperature outage alert
- recovery alert
- tampered reading rejected with HMAC verification failure

Screenshots containing HMAC secrets or credentials should not be committed.

## What I did not claim

My Week 7 GNS3 validation environment used a temporary flat switch/NAT path and a test broker listener with anonymous access enabled for connectivity testing.

Therefore I am **not** claiming that the following team-level tasks are complete yet:

- final GNS3 broker authentication enforcement
- final authenticated monitoring client
- topic ACLs
- final Pond A router/firewall topology
- final routing/segmentation
- Wireshark packet-capture evidence
- pH path
- DO migration into the final GNS3 path
- SAFE/HOLD controller integration

These remain Week 8 and later individual/integration tasks.

## How my work connects to the team

### Sahil Basnet — Sensor, Broker and Network Security

Sahil's technical workstream is responsible for the secured sensor/MQTT/network side, including broker hardening, authentication, ACLs, routing/segmentation and network-security evidence. My temporary broker/sensor nodes were only support infrastructure for testing my monitor.

### Neha Thanait — Monitoring and Trust Validation

My component receives sensor traffic after it reaches MQTT and decides whether the data can be trusted. I verify HMAC integrity, reject invalid/tampered readings, and detect trusted-data outage/recovery conditions.

### Md Monirul Haque Arnob — Control and Resilience

Arnob's SAFE/HOLD controller should consume trusted/invalid/outage state after my verification stage so unsafe control decisions are not made from untrusted raw MQTT data.

### Final integration relationship

```text
Sahil secured sensor/network/broker
              |
              v
Neha monitoring/trust validation
              |
              v
Arnob SAFE/HOLD/control
```

## Week 8 individual next work

My next tasks are:

1. keep developing/testing my own monitoring GNS3 environment
2. add monitoring-client authentication when the secured broker configuration is available
3. repeat valid/tampered/outage/recovery tests against the authenticated broker
4. perform security acceptance testing on the final routed Pond A integration path
5. capture monitoring-related network/Wireshark evidence
6. validate DO through my monitoring component when the integrated DO path is available
7. connect my trusted/outage output to Arnob's SAFE/HOLD component during final integration

## Simple explanation for mentoring

If asked what I personally did, I can explain it as:

> My individual part is security monitoring and trust validation. In Week 7 I built my own GNS3 validation environment and deployed my monitor on a separate Linux node. I also used temporary temperature and Mosquitto support nodes so I could independently test my component. My monitor accepted valid HMAC readings, rejected a tampered reading, detected an outage after 10 seconds and detected recovery when the sensor returned. The temporary sensor and broker were only used to test my monitor. Later my monitoring component will be integrated with Sahil's secured broker/network work and Arnob's SAFE/HOLD control work.

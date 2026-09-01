# Neha Thanait — Week 7 Individual Technical Progress

## Individual role

**Technical workstream:** Security Monitoring, Trust Validation and Security Testing

My responsibility is to make sure sensor data is checked before the system trusts it. My work focuses on verifying HMAC-protected sensor messages, rejecting tampered or malformed data, detecting sensor outages and recovery, logging security events, and proving these behaviours through tests.

## What I personally worked on in Week 7

During Week 7 I moved my monitoring and trust-validation work from the local prototype into GNS3 and tested it across separate virtual nodes.

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

### 2. Connected my monitor to a separate GNS3 Mosquitto broker

The monitor was changed from using only `localhost` to using the broker address supplied through the `AQ1_MQTT_BROKER` environment variable.

The monitor successfully connected to the separate broker node at:

`192.168.42.130:1883`

and subscribed to:

- `aquaculture/sensors/#`
- `aq1/pond1/#`

This proved that my monitoring component could operate from its own GNS3 Linux node rather than only from the original local Windows environment.

### 3. Verified valid temperature HMAC messages across GNS3

A separate `AQ1-TEMP-001-1` node published HMAC-protected temperature readings through the Mosquitto broker.

My monitor received the messages and accepted them only after successful HMAC verification.

Observed result:

`ACCEPTED | Sensor: TEMP-001 | Type: temperature | ... | HMAC: VALID`

**Result: PASS**

### 4. Tested temperature sensor outage detection across GNS3

I stopped the running temperature producer while keeping my monitoring node active.

After more than the configured 10-second timeout, my monitor reported:

`OUTAGE ALERT | Temperature sensor TEMP-001 unavailable | No valid reading for more than 10 seconds`

This confirmed that the per-sensor outage logic still worked when the sensor and monitor were running on separate GNS3 nodes.

**Result: PASS**

### 5. Tested recovery detection across GNS3

I restarted the temperature producer after the outage.

My monitor reported:

`RECOVERY | Temperature sensor TEMP-001 is online again`

and then resumed accepting valid signed readings.

**Result: PASS**

### 6. Tested tampered temperature rejection across GNS3

I used the controlled temperature tamper-test flow. The test created a valid HMAC for an original temperature reading, then modified the temperature value and status without recalculating the HMAC.

The modified payload travelled through the GNS3 MQTT broker, but my monitor rejected it because the received HMAC did not match the modified message contents.

Observed result:

`SECURITY ALERT | Temperature reading rejected | Sensor: TEMP-001 | Reason: HMAC verification failed`

**Result: PASS**

The invalid message did not reset the sensor health timer. This is intentional because invalid or forged data should not make a failed sensor appear healthy.

## My current GNS3 security flow

```text
AQ1-TEMP-001-1
      |
      v
AQ1-Mosquitto-Broker-1
      |
      v
Neha-Monitor-1
      |
      +--> valid signed reading -> ACCEPTED
      +--> tampered reading -> REJECTED
      +--> no valid reading > 10 seconds -> OUTAGE ALERT
      +--> valid reading returns -> RECOVERY
```

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

- `Neha-Monitor-1` running in GNS3
- `monitor.py` present and passing syntax validation
- successful monitor-to-broker connection
- valid `TEMP-001` readings accepted with `HMAC: VALID`
- temperature outage alert
- recovery alert
- tampered reading rejected with HMAC verification failure

Screenshots containing HMAC secrets or credentials should not be committed.

## What I did not claim

The Week 7 GNS3 test used a temporary flat switch/NAT path and a broker listener with anonymous access enabled for connectivity testing.

Therefore I am **not** claiming that the following are complete yet:

- GNS3 broker authentication enforcement
- authenticated monitoring client
- topic ACLs
- final Pond A router/firewall topology
- Wireshark packet-capture evidence
- pH path
- DO migration into GNS3
- SAFE/HOLD controller integration

These remain Week 8 and later integration tasks.

## How my work connects to the team

### Sahil Basnet

Sahil's sensor/MQTT/network-security work provides the producer, broker-security and network side that my monitor consumes and verifies.

### Md Monirul Haque Arnob

Arnob's SAFE/HOLD controller should consume trusted/invalid/outage state after verification so unsafe control decisions are not made from untrusted raw MQTT data.

### End-to-end relationship

`Sahil sensor/MQTT/network -> Neha monitoring/trust validation -> Arnob SAFE/HOLD/control`

## My next technical work

My next tasks are:

1. retest the monitoring path after broker authentication is enabled in GNS3
2. authenticate the monitoring client
3. repeat valid/tampered/outage/recovery tests on the final routed Pond A path
4. capture network/Wireshark evidence
5. validate DO in GNS3 when its node/path is added
6. integrate my trusted/outage output with Arnob's SAFE/HOLD controller

## Simple explanation for mentoring

If asked what I personally did, I can explain it as:

> My part is security monitoring and trust validation. I moved my monitor into a separate GNS3 Linux node and connected it to a separate Mosquitto broker. I tested valid HMAC-protected temperature readings, tampered readings, sensor outage and recovery. Valid readings were accepted, tampered readings were rejected, stopping the sensor caused an outage alert after 10 seconds, and restarting it produced a recovery alert. My next step is to repeat these tests with GNS3 MQTT authentication, ACLs, the routed Pond A network and later SAFE/HOLD integration.

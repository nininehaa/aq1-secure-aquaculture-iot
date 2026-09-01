# Week 7 GNS3 Temperature-to-Monitor Validation

## Purpose

Record the first working AQ-1 temperature security path across separate GNS3 nodes completed as Week 7 technical progress, and distinguish what was actually demonstrated from what is still pending.

## GNS3 nodes used

The Week 7 validation used separate Docker/Alpine nodes in GNS3:

```text
AQ1-TEMP-001-1
      |
      v
    Switch1
   /       \
  v         v
AQ1-Mosquitto-Broker-1    Neha-Monitor-1
      |
     NAT3 (temporary package-install/internet access)
```

Observed addresses during the test:

- Mosquitto broker: `192.168.42.130`
- TEMP-001: `192.168.42.144`
- monitoring node: DHCP address on the same temporary GNS3 NAT/switch network

`NAT3` was used for package installation and temporary connectivity. It is not the final Pond A router/firewall design.

## Monitoring node preparation

`Neha-Monitor-1` was prepared with:

- Alpine Linux container
- Python 3
- Python virtual environment
- `paho-mqtt`
- project `monitor.py` in `/opt/aq1/monitor.py`

Validation performed:

```text
python -m py_compile monitor.py
```

completed without a syntax error, and `paho.mqtt.client` imported successfully.

The monitor was configured to use the GNS3 broker address instead of localhost and successfully connected to:

```text
192.168.42.130:1883
```

It subscribed to:

- `aquaculture/sensors/#`
- `aq1/pond1/#`

## Broker node preparation

`AQ1-Mosquitto-Broker-1` was prepared with:

- Alpine Linux container
- Mosquitto 2.1.2
- Mosquitto client tools

For the first GNS3 connectivity/security-flow validation, a temporary listener was configured on TCP port 1883 with anonymous access enabled so the virtualised MQTT/HMAC path could be proven before restoring authentication controls.

Therefore this test **does not claim that GNS3 broker authentication is enforced yet**. Broker authentication, monitoring-client credentials and topic ACLs remain separate hardening tasks.

## TEMP-001 node preparation

`AQ1-TEMP-001-1` was prepared with:

- Alpine Linux container
- Python 3
- Python virtual environment
- `paho-mqtt`
- project `temperature_sensor.py`
- project `temperature_tamper_test.py`

The producer was configured to publish to the GNS3 Mosquitto broker at `192.168.42.130` and to use the existing project temperature HMAC key.

## Tests performed

### 1. Valid signed temperature readings — PASS

TEMP-001 published HMAC-SHA256 protected readings through Mosquitto.

The monitor received and accepted the readings with output of the form:

```text
ACCEPTED | Sensor: TEMP-001 | Type: temperature | ... | HMAC: VALID
```

This proves the signed temperature message travelled from the separate TEMP-001 node through the separate broker node to the separate monitoring node and passed HMAC verification.

### 2. Temperature outage detection — PASS

The running `temperature_sensor.py` process was stopped while the monitor remained active.

After the configured 10-second threshold, the monitor reported:

```text
OUTAGE ALERT | Temperature sensor TEMP-001 unavailable | No valid reading for more than 10 seconds
```

### 3. Temperature recovery — PASS

The temperature producer was restarted after the outage.

The monitor reported:

```text
RECOVERY | Temperature sensor TEMP-001 is online again
```

and then resumed accepting valid signed readings.

### 4. Temperature tamper rejection — PASS

The controlled tamper test created a valid HMAC for an original reading of `27.2 C / NORMAL`, then changed the payload to `41.2 C / HIGH` without recalculating the HMAC.

The modified payload was published through the GNS3 broker. The monitor rejected it with:

```text
SECURITY ALERT | Temperature reading rejected | Sensor: TEMP-001 | Reason: HMAC verification failed
```

The tampered message did not reset the valid-reading health timer. This is intentional: invalid data cannot keep a failed or compromised sensor marked healthy.

## Result

The following GNS3 security flow was demonstrated in Week 7:

```text
TEMP-001
   |
   v
Mosquitto broker
   |
   v
Neha monitoring / trust validation
   |
   +--> valid signed reading -> ACCEPTED
   +--> sensor stopped -> OUTAGE ALERT
   +--> valid sensor returns -> RECOVERY
   +--> tampered signed payload -> REJECTED
```

## What is not yet complete

This is an important first virtualised end-to-end slice, but it is not the complete Pond A MVP. Remaining work includes:

- replace the temporary flat switch/NAT path with the planned Pond A routed/router-firewall topology
- restore and verify broker-side MQTT authentication in GNS3
- authenticate the monitoring client
- implement and test topic ACLs
- capture GNS3/Wireshark network evidence
- move/validate DO on the GNS3 path
- implement and validate pH
- integrate Arnob's SAFE/HOLD controller

## Evidence handling

Runtime screenshots were captured during the test showing valid HMAC acceptance, outage, recovery, and tamper rejection. Screenshots containing secrets should not be committed. Only clean evidence that does not expose HMAC keys or credentials should be added to the repository.

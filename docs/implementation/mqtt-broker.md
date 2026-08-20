# MQTT Broker and Authentication

## Purpose

Eclipse Mosquitto is used as the MQTT broker between the simulated sensors and the components that receive their readings.

The broker acts as the message-routing point for the prototype.

```text
Sensor publisher -> Mosquitto broker -> Subscriber / Monitor
```

## Current Configuration

The current broker configuration is stored at:

`configs/mosquitto/mosquitto.conf`

The secure listener uses TCP port `1883`.

Anonymous access is disabled.

The local password file is not committed to GitHub and is excluded through `.gitignore`.

## Why Authentication Was Added

The first MQTT prototype focused on basic publish/subscribe communication. For a security project, allowing anonymous clients would mean any reachable device could attempt to connect without proving its identity.

MQTT authentication was therefore added so the broker can distinguish authorised and unauthorised clients.

## Current Authentication Flow

```text
Client connects
      |
      v
Mosquitto checks credentials
      |
 +----+----+
 |         |
valid    missing/invalid
 |         |
allow     reject
```

The temperature sensor uses credentials supplied through environment variables rather than storing the password directly in the Python file.

## Tests Completed

### Authorised client

An MQTT subscriber using the configured credentials was able to connect and receive live temperature readings from:

`aq1/pond1/temperature`

**Result:** PASS

### Client with no credentials

A subscriber was started without a username or password.

Observed result:

`Connection Refused: not authorised`

**Result:** PASS

This demonstrates that anonymous MQTT access is not permitted by the current secure broker configuration.

## Broker Status Verification

The local listener was checked using PowerShell:

```powershell
Get-NetTCPConnection -LocalPort 1883 -State Listen
```

A listening entry on port `1883` confirms that the MQTT broker is running and accepting connection attempts on that port.

## Current Limitations

The current configuration is suitable for the local prototype but is not yet the final deployment design.

Remaining work includes:

- give the monitoring client its own MQTT credentials
- standardise MQTT topic naming
- add topic-level ACL rules
- make the configuration portable rather than depending on a local Windows password-file path
- add TLS so MQTT traffic is encrypted in transit
- deploy the broker as a separate node in GNS3
- later test primary/backup broker resilience

## Security Responsibilities

MQTT authentication answers:

**Is this client allowed to connect?**

It does not replace HMAC. HMAC answers a different question:

**Has the protected sensor message been changed?**

The project uses both controls because connection authentication and message integrity solve different security problems.

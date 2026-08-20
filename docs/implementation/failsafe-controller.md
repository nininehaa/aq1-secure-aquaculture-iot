# Fail-Safe Controller

## Purpose

The fail-safe controller is the part of the project that decides what the aquaculture control system should do when trusted sensor information is unavailable or invalid.

The aim is to prevent unsafe automatic actions from being triggered by data that the system cannot trust.

## Intended Behaviour

```text
Trusted sensor data
        |
        v
     NORMAL
        |
        v
Automatic control allowed
```

If a required reading is invalid, tampered or unavailable:

```text
Untrusted / missing data
          |
          v
       SAFE/HOLD
          |
          v
Unsafe automatic action blocked
```

## Inputs to the Controller

The controller should use the result of security monitoring rather than blindly trusting raw MQTT data.

Examples of conditions that should influence the controller are:

- valid trusted sensor reading
- invalid HMAC / tampered message
- sensor outage
- broker/service failure
- recovery of valid trusted sensor data

## Expected State Flow

1. Valid trusted data is available -> `NORMAL`.
2. Required trusted data becomes invalid or unavailable -> `SAFE/HOLD`.
3. The system remains in `SAFE/HOLD` while the problem continues.
4. Valid trusted readings recover -> controlled recovery.
5. After recovery conditions are satisfied -> return to `NORMAL`.

## Simulated Equipment

The final prototype may represent actions such as:

- aerator control
- pump control
- feeder control

The project does not need to operate real farm equipment. The important point is to demonstrate that untrusted cyber data cannot directly cause an unsafe simulated control action.

## Current Status

**Status: In development / integration pending.**

The fail-safe controller should not be described as completed until the team has implemented and tested the `SAFE/HOLD` state transitions.

The current Week 6 test plan records the fail-safe activation test as pending.

## Planned Test Cases

### Normal case

Valid trusted sensor readings -> controller remains `NORMAL`.

### Tamper case

A sensor message fails security verification -> unsafe automatic action is blocked and the controller enters or remains in `SAFE/HOLD` as required.

### Outage case

A required trusted sensor stops providing valid readings -> controller enters `SAFE/HOLD`.

### Recovery case

Valid trusted readings return -> controller performs a controlled recovery before returning to `NORMAL`.

## Integration Dependency

The controller depends on the monitoring component providing a clear trusted/untrusted or availability state.

This creates the final project chain:

```text
Sensor / MQTT security
        |
        v
Trust validation / monitoring
        |
        v
SAFE/HOLD controller
        |
        v
Simulated farm action
```

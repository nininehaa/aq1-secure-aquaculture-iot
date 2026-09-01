# Week 7 Project Progress

## Reporting period
24–30 August 2026

## Main focus
Week 7 focused on consolidating the project after the Week 6 security prototype, improving engineering documentation, and preparing a clearer transition from the local prototype to GNS3.

## Technical position carried forward
The strongest tested local slice remained:

```text
DO / Temperature producer
        |
        v
Mosquitto MQTT broker
        |
        v
Security monitoring / HMAC verification
        |
        v
Trusted / rejected / outage decision
```

No GNS3 routed end-to-end path or SAFE/HOLD implementation is claimed as completed in this week.

## Engineering and documentation work completed

The repository was expanded with shared engineering records so implementation, ownership and evidence can be reviewed more systematically:

- implementation-status source of truth
- requirements traceability matrix
- live project risk register
- weekly engineering-review template
- project evidence index improvements
- GNS3 deployment design and planned addressing
- consolidated security-test results
- implementation/setup/troubleshooting documentation
- project decisions and team-role documentation

## Why this work was needed
The project had working technical pieces, but information was spread across code, tests, issues and older documents. The Week 7 documentation work aimed to make it easier to answer:

1. what is actually implemented and tested
2. what is still pending
3. who owns each technical area
4. where the evidence is located
5. what the next implementation milestone is

## Current member workstreams

- **Sahil Basnet:** sensor/MQTT/network-security work, broker authentication, topic/ACL work and GNS3 network path.
- **Neha Thanait:** security monitoring, HMAC verification, outage/recovery, security testing and verification evidence.
- **Md Monirul Haque Arnob:** SAFE/HOLD control and resilience integration.

## Remaining technical priorities

- authenticate the monitoring client against the secured broker
- standardise MQTT topics and implement topic ACLs
- implement and test SAFE/HOLD
- build the first routed GNS3 Pond A path
- add the pH path to complete the three-sensor project scope
- capture GNS3/Wireshark evidence

## Week 7 outcome
Week 7 improved project traceability and documentation quality, but it did not replace the need for practical implementation. The next phase remains the one-Pond-A GNS3 MVP and SAFE/HOLD integration.

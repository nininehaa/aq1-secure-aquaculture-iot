# AQ-1 Project Documentation

This folder contains the working documentation for the Coral Coast Aquaculture secure IoT project.

The documentation is written so that another student, tutor or developer can understand what the team is building, what has already been implemented, how it was tested, what problems were found, and what is still planned.

## Start Here

1. [Project overview](project-overview.md) — why the project exists and what problem it solves.
2. [Team roles](team-roles.md) — who is responsible for each technical area.
3. [Current architecture](architecture/current-week6-architecture.md) — current working prototype and GNS3 scale-up direction.
4. [Local demo setup](setup/local-demo-setup.md) — how to reproduce the current secure MQTT temperature demo.
5. [Project decisions](project-decisions.md) — important technical choices and why they were made.
6. [Troubleshooting log](troubleshooting.md) — implementation problems, investigation and resolution.
7. [Project evidence index](evidence-index.md) — where the code, tests, commits and documentation for each project area can be found.

## Implementation Documentation

- [Dissolved-oxygen sensor](implementation/dissolved-oxygen-sensor.md)
- [Temperature sensor](implementation/temperature-sensor.md)
- [MQTT broker and authentication](implementation/mqtt-broker.md)
- [Monitoring and verification](implementation/monitoring.md)
- [Fail-safe controller](implementation/failsafe-controller.md)

## Security Documentation

- [Security design](security/security-design.md)
- [Threat model](security/threat-model.md)
- [Temperature MQTT and HMAC security](security/temperature-mqtt-security.md)

## Testing

- [Week 6 Security Test Plan](../testing/Week_6_Security_Test_Plan.md)
- [Consolidated security test results](../testing/security-test-results.md)
- [Week 5 Test Plan](../testing/week5_test_plan.md)

## GNS3 Network Scale-Up

- [GNS3 deployment design](gns3/gns3-design.md)
- [Planned network addressing](gns3/network-addressing.md)

These GNS3 documents are clearly marked as planned/in progress until the virtual network is actually implemented and tested.

## Progress Records

- [Week 5 progress](progress/week-5.md)
- [Week 6 progress](progress/week-6.md)
- [Sahil Week 6 implementation record](progress/sahil-week6-progress.md)

## Documentation Rule

For each meaningful project change, the team should record:

1. Why the work was needed.
2. What was implemented or changed.
3. How it works.
4. How it was tested.
5. What result was observed.
6. What remains to be done.

Code and screenshots are evidence, but the documentation explains the purpose, design and result of that evidence.

## Status Language

To keep the project honest and easy to review, documentation should use clear status labels:

- **Implemented** — working code/configuration exists.
- **Tested / PASS** — a recorded test was performed successfully.
- **In progress** — work has started but is not complete.
- **Planned** — design or future work only.
- **Pending** — required work/test has not yet been completed.

This prevents planned features from being mistaken for finished implementation.

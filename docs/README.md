# AQ-1 Project Documentation

This folder contains the working documentation for the Coral Coast Aquaculture secure IoT project.

The documentation is written so that another student, tutor or developer can understand what the team is building, what has already been implemented, how it was tested, what problems were found, and what is still planned.

## Start Here

1. [Project overview](project-overview.md) — why the project exists and what problem it solves.
2. [Team roles](team-roles.md) — who is responsible for each technical area.
3. [Implementation status](project-management/implementation-status.md) — single source of truth for what is implemented, tested, in progress or pending.
4. [Requirements traceability](project-management/requirements-traceability.md) — links requirements to owners, implementation and acceptance evidence.
5. [Risk register](project-management/risk-register.md) — current technical, delivery and evidence risks.
6. [Current architecture](architecture/current-week6-architecture.md) — current working prototype and GNS3 scale-up direction.
7. [Local demo setup](setup/local-demo-setup.md) — how to reproduce the current secure MQTT demo.
8. [Project decisions](project-decisions.md) — important technical choices and why they were made.
9. [Troubleshooting log](troubleshooting.md) — implementation problems, investigation and resolution.
10. [Project evidence index](evidence-index.md) — where code, tests, commits and documentation can be found.

## Project Management and Engineering Control

- [Implementation status](project-management/implementation-status.md)
- [Requirements and traceability matrix](project-management/requirements-traceability.md)
- [Risk register](project-management/risk-register.md)
- [Weekly engineering review template](project-management/weekly-review-template.md)

The project-management files are live engineering records. They should be updated when implementation status, scope, risk, ownership or acceptance evidence changes.

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

These GNS3 documents must remain marked planned/in progress until the virtual network is actually implemented and tested.

## Progress Records

- [Week 5 progress](progress/week-5.md)
- [Week 6 progress](progress/week-6.md)

Individual contribution evidence should be created and committed by the relevant team member, while shared project records should remain factual and team-oriented.

## Documentation Rule

For each meaningful project change, record:

1. Why the work was needed.
2. What was implemented or changed.
3. How it works.
4. How it was configured/run.
5. How it was tested.
6. What result was observed.
7. Where the evidence is located.
8. What remains to be done.

Code and screenshots are evidence, but the documentation explains the purpose, design, implementation and result of that evidence.

## Definition of Done

For this project, **code alone is not implementation evidence**. A feature is complete only when it is:

**built + configured + run + tested + evidenced + documented**.

Where applicable, the requirement should also be linked to a GitHub issue/card, implementation commit/PR and acceptance test.

## Status Language

To keep the project honest and easy to review, documentation should use clear status labels:

- **Implemented** — working code/configuration exists.
- **Tested / PASS** — a recorded test was performed successfully.
- **In progress** — work has started but is not complete.
- **Planned** — design or future work only.
- **Pending** — required work/test has not yet been completed.

This prevents planned features from being mistaken for finished implementation.

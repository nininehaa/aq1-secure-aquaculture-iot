# AQ-1 Project Documentation

This folder contains the working documentation for the Coral Coast Aquaculture secure IoT project.

The documentation is organised so the team, tutor and reviewers can quickly answer four questions:

1. What are we building?
2. What actually works now?
3. Who owns each technical area?
4. What remains before the final demo?

## Start Here

Read these in this order:

1. [Current project plan](project-management/project-plan.md) — **main delivery plan**, including one-Pond-A MVP, ownership, delivery order and stretch goals.
2. [Implementation status](project-management/implementation-status.md) — **single source of truth for what actually works today**.
3. [Team roles](team-roles.md) — who is responsible for each technical workstream.
4. [Project overview](project-overview.md) — business problem, security goal and prototype background.
5. [Requirements traceability](project-management/requirements-traceability.md) — requirement-to-owner-to-implementation/test/evidence mapping.
6. [Risk register](project-management/risk-register.md) — current technical, delivery and evidence risks.
7. [Current Week 6 architecture](architecture/current-week6-architecture.md) — historical/current-prototype architecture plus the documented scale-up direction.
8. [Local demo setup](setup/local-demo-setup.md) — how to reproduce the current local secure MQTT demo.
9. [Project decisions](project-decisions.md) — important technical choices and why they were made.
10. [Troubleshooting log](troubleshooting.md) — implementation problems, investigation and resolution.
11. [Project evidence index](evidence-index.md) — where code, tests, commits and documentation can be found.

## Important Scope Clarification

The current project plan separates the **MVP** from **future scale-up**.

### Immediate MVP

The immediate implementation target is **one Pond A GNS3 path** using the project sensor scope of dissolved oxygen, temperature and pH.

The current local prototype already has working DO and temperature paths. The pH path remains to be implemented/tested.

The first routed GNS3 milestone may begin with `TEMP-001` and then expand the Pond A implementation.

### Future scale-up / stretch

The following are not the immediate first GNS3 requirement:

- Pond B and Pond C
- backup MQTT broker
- larger attacker/test network
- extra feeder/sensor identities
- advanced Node-RED dashboard features
- TLS/stronger key management
- broker failover/redundancy and larger-scale load tests

These should remain marked **Planned** or **In progress** until implemented and evidenced.

## Project Management and Engineering Control

- [Current project plan](project-management/project-plan.md)
- [Implementation status](project-management/implementation-status.md)
- [Requirements and traceability matrix](project-management/requirements-traceability.md)
- [Risk register](project-management/risk-register.md)
- [Weekly engineering review template](project-management/weekly-review-template.md)

The project-management files are live engineering records. When implementation status, scope, risk, ownership or acceptance evidence changes, update the appropriate existing record rather than creating a competing version of the plan.

## Design Documentation

- [Monitoring and trust-validation design — Neha](design/monitoring-trust-validation-design.md)

Each major technical workstream should have a design document that explains intended behaviour, interfaces, normal and failure flows, security controls, design decisions, assumptions/limitations and acceptance criteria. Design documentation should be linked to the corresponding implementation and test evidence.

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

## GNS3 Network Work

- [GNS3 deployment design](gns3/gns3-design.md)
- [Planned network addressing](gns3/network-addressing.md)
- [Week 7 TEMP-001 to monitor validation](gns3/week7-temp-monitor-validation.md)

These GNS3 documents distinguish planned scale-up from demonstrated runtime evidence. The **first required practical milestone remains the one-Pond-A routed path** defined in the current project plan.

## Progress Records

- [Week 5 progress](progress/week-5.md)
- [Week 6 progress](progress/week-6.md)
- [Week 7 progress](progress/week-7.md)
- [Neha Week 7 individual technical progress](progress/neha-week7-individual-progress.md)
- [Week 8 progress and priorities](progress/week-8.md)

Weekly records should continue in this folder so the repository shows sustained development and clearly separates actual technical progress from planning/documentation work.

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

Use the following consistently:

- **Implemented** — working code/configuration exists.
- **Tested / PASS** — a recorded test was performed successfully.
- **In progress** — work has started but is not complete.
- **Planned** — design or future work only.
- **Pending** — required work/test has not yet been completed.

This prevents future architecture or stretch goals from being mistaken for finished implementation.

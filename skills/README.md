# Agent Skills

Skills are reusable, version-controlled engineering workflows that help AI agents perform specialised activities consistently.

They are designed to remain portable across coding agents wherever practical.

> Standards define what good engineering looks like.
> Skills define how an agent performs a particular engineering activity.

Skills must not become substitutes for engineering standards, policies or automated controls.

## Design Principles

A skill should be:

- focused on one engineering capability
- reusable across repositories and technologies
- independent of a specific AI vendor where practical
- explicit about inputs and outputs
- aware of applicable standards and policies
- proportionate to engineering risk
- auditable through predictable outputs
- small enough to evolve safely

Avoid embedding large technology-specific rule sets inside skills.

For example:

```text
skills/test/
```

may define how an agent develops a testing strategy.

Rules such as minimum test expectations, approved testing patterns or mandatory security tests belong under:

```text
standards/testing/
policies/
```

## Initial Skills

The platform currently defines:

```text
grill
architecture-review
implement
test
security-review
production-readiness
interview-me
```

### grill

Adversarially challenges requirements, architecture proposals and implementation plans before engineering effort is committed.

### architecture-review

Evaluates a proposed or implemented architecture against architectural drivers, standards and known constraints.

### implement

Turns an approved requirement or design into a focused production-quality change.

### test

Designs and executes risk-based verification of a change.

### security-review

Examines a change for security risks, trust-boundary violations and applicable security requirements.

### production-readiness

Determines whether a system or change is operationally ready to run safely in production.

### interview-me

Transforms implementation and architecture experience into structured technical interview practice.

## Skill Invocation

Agents may expose skills differently.

Examples include:

```text
/grill
/architecture-review
/implement
/test
/security-review
/production-readiness
/interview-me
```

The invocation mechanism is agent-specific.

The behaviour defined by the skill should not be.

## Skill Execution

Before executing a skill:

1. understand the requested outcome
2. inspect relevant repository context
3. identify applicable standards
4. identify applicable policies
5. inspect relevant architectural decisions
6. execute the specialised workflow
7. clearly report unresolved risks or validation gaps

Do not assume the absence of context means there are no constraints.

## Skill Composition

Skills may be used together.

For substantial engineering work, the normal flow is:

```text
grill
  ↓
architecture-review
  ↓
implement
  ↓
test
  ↓
security-review
  ↓
production-readiness
```

This is a workflow, not a mandatory pipeline.

Low-risk changes may require only a subset.

## Decision Ownership

Skills may recommend decisions.

They do not automatically authorise high-risk decisions.

Human approval remains required where defined by:

- repository policy
- organisational governance
- security controls
- production change controls

## Skill Evolution

When changing a skill:

- preserve its core responsibility
- avoid quietly expanding its authority
- avoid duplicating standards
- consider existing consumers
- test the changed workflow against real engineering work

Skills should improve based on lessons from actual projects.

# Architecture Decision Records

## Purpose

This directory contains Architecture Decision Records (ADRs) for significant and durable engineering decisions.

ADRs exist to preserve the reasoning behind important decisions so future engineers and AI agents can understand:

- what was decided
- why it was decided
- which alternatives were considered
- which trade-offs were accepted

ADRs should not become a diary of routine implementation choices.

## When to Create an ADR

Create an ADR when a decision materially affects:

- system architecture
- domain boundaries
- data ownership
- integration patterns
- security boundaries
- tenancy
- technology strategy
- deployment architecture
- engineering platform design
- significant vendor dependency
- long-term portability
- governance or control architecture

Examples include:

```text
Choose modular monolith instead of microservices
Use asynchronous events for cross-domain integration
Select tenant-isolation strategy
Adopt a particular identity architecture
Introduce an event broker
Adopt a specific database model
Define the engineering control architecture
```

## When Not to Create an ADR

An ADR is usually unnecessary for:

- routine refactoring
- naming decisions
- minor dependency upgrades
- small implementation details
- reversible low-impact choices
- ordinary defect fixes

## ADR Lifecycle

Use the following statuses:

```text
PROPOSED
ACCEPTED
SUPERSEDED
DEPRECATED
REJECTED
```

### PROPOSED

The decision is under consideration.

### ACCEPTED

The decision has been approved and should guide implementation.

### SUPERSEDED

A newer ADR replaces this decision.

The replacing ADR should be referenced.

### DEPRECATED

The decision is no longer recommended but may still exist in deployed systems.

### REJECTED

The proposal was evaluated but deliberately not adopted.

## Naming

Use:

```text
NNNN-short-decision-title.md
```

Examples:

```text
0001-agent-portability-strategy.md
0002-engineering-control-model.md
0003-multi-tenant-data-isolation.md
```

Numbers should be sequential.

## ADR Structure

Use:

```text
docs/decisions/0000-adr-template.md
```

The standard structure is:

```text
Title
Status
Date
Context
Decision
Alternatives Considered
Consequences
Validation
Related Controls / Standards
```

## Decision Quality

An ADR should explain the decision sufficiently for someone who was not present during the original discussion.

Prefer concise reasoning over large documentation.

The most important sections are:

```text
Why was the decision necessary?
Why was this option selected?
What did we give up?
What consequences must future engineers understand?
```

## Relationship to Grill

For material architectural work:

```text
Requirement
    ↓
Grill
    ↓
Options / Trade-offs
    ↓
Decision
    ↓
ADR
```

`grill` challenges the proposal.

The ADR records the resulting durable decision.

## Relationship to Architecture Review

Architecture review may identify that an ADR is required.

The architecture-review skill should verify relevant existing ADRs before recommending architectural changes.

## Relationship to Controls

Where an ADR introduces a durable constraint that can be automatically checked, consider creating an engineering control.

Example:

```text
ADR:
Domain A must not reference Domain B directly
        ↓
Architecture rule
        ↓
ARC-005 Architecture Test
```

Not every ADR requires an automated control.

## AI Agents

AI agents should:

- inspect relevant ADRs before significant architectural changes
- recommend ADR creation when a decision is sufficiently consequential
- avoid creating ADRs for trivial choices
- identify when an existing ADR may need to be superseded

AI agents must not silently ignore an accepted ADR.

If a task conflicts with an accepted ADR, surface the conflict.

## Architectural Principle

ADRs record decisions.

They do not replace:

- standards
- policies
- controls
- source code
- architecture diagrams

They preserve the reasoning that those other assets cannot fully express.

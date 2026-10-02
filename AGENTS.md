# Agentic Engineering Platform

This repository is an engineering platform for building production-grade software with AI-assisted development.

The core principle is:

> Standards are durable; agents are replaceable.

The repository should remain portable across coding agents wherever practical. Agent-specific configuration must not become the primary source of engineering rules.

## Working Principles

All contributors, including AI agents, must:

- prefer production-grade solutions over demos or shortcuts
- follow repository engineering standards and policies
- make assumptions explicit
- challenge unclear or risky requirements before implementation
- prefer simple designs over unnecessary abstraction
- preserve portability across supported development agents
- separate guidance from enforceable controls
- treat security, testing, observability and operability as implementation concerns, not follow-up tasks
- avoid introducing technologies or architectural patterns without a justified need
- make consequential architectural decisions explicit
- require human approval for high-risk or irreversible actions

## Sources of Authority

Use repository guidance in this order:

1. applicable policies
2. engineering standards
3. approved architecture decisions
4. task-specific requirements
5. reusable skills
6. agent-specific configuration

A skill may guide how work is performed but must not override repository standards or policies.

If instructions conflict, stop and surface the conflict rather than silently choosing one.

## Repository Structure

```text
skills/          Reusable agent workflows and specialised capabilities
standards/       Durable organisational engineering standards
policies/        Mandatory governance and control requirements
templates/       Reusable implementation and documentation templates
scripts/         Automation used by developers and CI
docs/decisions/  Significant architectural decisions and trade-offs
```

Do not duplicate standards inside skills. Skills should reference applicable standards instead.

## Development Workflow

For substantial changes, use the following default flow:

```text
Understand
   ↓
Grill
   ↓
Decide
   ↓
Implement
   ↓
Test
   ↓
Security Review
   ↓
Automated Quality Gates
   ↓
Production Readiness
   ↓
Human Approval where required
```

Not every trivial change requires every stage. Apply engineering judgment proportionate to risk.

## Before Implementation

Before writing code:

- understand the user or business outcome
- identify relevant standards and policies
- identify architectural and operational constraints
- identify assumptions and unresolved decisions
- use the `grill` skill for material changes where requirements or design need challenge

Do not begin substantial implementation while critical design questions remain unresolved.

## Implementation Expectations

During implementation:

- keep changes focused
- reuse existing conventions before introducing new ones
- avoid speculative abstractions
- maintain backwards compatibility unless a breaking change is explicitly approved
- include appropriate tests with the change
- handle failures deliberately
- avoid logging secrets or sensitive information
- make external dependencies explicit
- consider security boundaries and trust boundaries
- consider observability and operational support
- update relevant decisions or documentation when architecture meaningfully changes

## Verification

A change is not complete because code was generated successfully.

Verification should include the applicable subset of:

- build
- static analysis
- formatting/linting
- unit tests
- integration tests
- contract tests
- architecture tests
- security scanning
- dependency scanning
- secret scanning
- infrastructure validation
- deployment validation

Automated controls are authoritative where they exist.

Do not bypass failing quality gates unless an explicitly documented and approved exception exists.

## Architectural Decisions

Create or update an architectural decision when a change:

- materially affects system structure
- introduces a significant technology
- changes a major integration pattern
- creates an important long-term constraint
- changes a security or tenancy boundary
- involves a meaningful trade-off that future engineers will need to understand

Do not create ADRs for routine implementation details.

## Risk and Human Approval

Human approval is required before actions such as:

- production deployment
- destructive data operations
- credential or identity changes
- security-policy changes
- externally visible breaking changes
- major infrastructure deletion or replacement
- changes with significant financial or regulatory impact

When uncertain whether an action is high risk, surface the risk instead of proceeding silently.

## Agent Behaviour

Agents should act as engineering collaborators, not code generators.

When relevant:

- explain important trade-offs
- identify risks early
- challenge weak assumptions
- propose alternatives when they materially improve the outcome
- distinguish facts from assumptions
- identify when validation is still required
- avoid false confidence

Prefer concise reasoning and actionable engineering output over lengthy generic explanation.

## Skills

Reusable workflows are located under `skills/`.

Use a skill when its purpose matches the task.

Initial platform skills include:

```text
grill
architecture-review
implement
test
security-review
production-readiness
interview-me
```

Skills are versioned engineering assets and should evolve based on lessons learned from real projects.

## Continuous Improvement

When a prototype exposes a recurring engineering problem:

1. determine whether the problem belongs in a standard, policy, skill, template, or automated control
2. improve the platform rather than solving the same problem repeatedly inside individual projects
3. prefer enforceable automation when a rule can be reliably machine-verified

The platform should become stronger through use.
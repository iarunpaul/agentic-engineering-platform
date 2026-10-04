# Engineering Controls

## Purpose

The `controls/` directory connects organisational engineering expectations to verifiable enforcement.

The platform separates:

- standards — how engineering should be performed
- policies — mandatory constraints
- skills — how agents perform engineering activities
- controls — how requirements are verified or enforced
- evidence — proof that a control was evaluated

The core flow is:

```text
Standard / Policy
        ↓
Control
        ↓
Execution
        ↓
Evidence
        ↓
Decision
```

## Core Principle

> Guidance influences behaviour. Controls provide evidence.

An instruction in `AGENTS.md`, a skill, or a standard does not by itself prove compliance.

Where a requirement can be objectively verified, prefer an automated control.

Where engineering judgement is required, use an explicit review control.

## Control Types

Controls fall into four categories.

### Automated

Executed automatically by tooling.

Examples:

- build
- automated tests
- secret scanning
- dependency scanning
- API contract validation

### Review

Requires engineering judgement.

Examples:

- architecture review
- security review
- production-readiness review
- test adequacy review

### Approval

Requires explicit authorised human approval.

Examples:

- production deployment
- quality-gate exception
- destructive data operation
- breaking external contract change

### Preventive

Prevents prohibited behaviour before execution.

Examples:

- protected branches
- protected deployment environments
- least-privilege permissions
- mandatory pull-request reviews

A control may belong to more than one category where appropriate.

## Control Outcomes

Controls should report one of:

```text
PASS
FAIL
WARN
NOT_APPLICABLE
NOT_EXECUTED
```

### PASS

The control was executed and its acceptance criteria were satisfied.

### FAIL

The control was executed and its acceptance criteria were not satisfied.

### WARN

The control found a non-blocking condition requiring attention.

### NOT_APPLICABLE

The control does not apply to this change or system.

Where a control would normally be expected, the reason should be recorded.

### NOT_EXECUTED

The control applies but was not executed.

`NOT_EXECUTED` must never be interpreted as `PASS`.

## Enforcement Levels

Controls may be:

```text
BLOCKING
NON_BLOCKING
CONDITIONAL
```

### BLOCKING

Failure prevents merge, release, deployment, or another protected transition.

### NON_BLOCKING

Failure or warning provides engineering information but does not automatically prevent progression.

### CONDITIONAL

The control applies or becomes blocking only when relevant conditions are met.

Examples include:

- environment
- risk classification
- affected component
- technology
- change type
- security impact
- architecture impact
- severity

Conditional controls must not be silently skipped.

## Control Ownership

Each control must have:

- stable control ID
- clear purpose
- source standard or policy
- control type
- execution stage
- enforcement behaviour
- expected evidence

Controls should remain implementation-neutral at the catalogue level.

For example:

```text
SEC-001 Secret Detection
```

is the organisational control.

The implementation might use:

```text
Gitleaks
GitHub Secret Scanning
another approved scanner
```

The tool may change without changing the organisational control identity.

## Stable Control IDs

Control IDs use domain prefixes.

```text
ENG  Engineering
TST  Testing
SEC  Security
API  API
OBS  Observability
ARC  Architecture
AI   AI-assisted engineering
REL  Release / production readiness
GOV  Governance
```

Examples:

```text
ENG-001
SEC-001
ARC-002
GOV-001
```

Control IDs must remain stable once published.

Retired IDs should not be reused for unrelated controls.

## Source Traceability

Every control should identify the organisational requirement that created it.

Examples:

```text
policies/secrets.md
standards/testing/testing-standard.md
standards/security/secure-engineering.md
```

A requirement may map to multiple controls.

For example:

```text
Secrets must not be committed
        ↓
SEC-001 Secret Detection
SEC-008 Secret Exposure Response
```

Likewise, a control may help satisfy more than one requirement.

## Control Catalogue

The machine-readable control catalogue is:

```text
controls/catalog.yaml
```

It is intended to describe:

- control identity
- control name
- source requirement
- control type
- execution stage
- enforcement behaviour
- evidence type

The catalogue should remain independent of any specific CI vendor or scanner where practical.

## Human-Readable Matrix

The human-readable governance view is:

```text
controls/control-matrix.md
```

It maps organisational requirements to:

- controls
- enforcement
- evidence
- execution stages

The matrix and catalogue must remain aligned.

Until this alignment is automated, changes to one should be reflected in the other.

## Evidence

Each control execution should produce or reference evidence.

Evidence may include:

- command output
- CI job result
- test report
- scanner report
- architecture review decision
- security review decision
- approval record
- deployment result
- artifact digest

Evidence requirements are defined under:

```text
evidence/
```

The common evidence contract is defined in:

```text
evidence/evidence-contract.md
```

The machine-readable schema is:

```text
evidence/schema/control-evidence.schema.json
```

## Evidence Principle

> No evidence means no verified control outcome.

For example:

```text
"The tests should pass."
```

is not evidence.

This is evidence:

```text
TST-001
    ↓
CI test execution
    ↓
machine-readable test report
    ↓
PASS
```

Likewise:

```text
"Security looks fine."
```

is not sufficient evidence for an automated security control.

Agents may summarise evidence, but they must not fabricate or replace it.

## Control Execution Stages

Controls should run as early as practical.

Typical stages include:

```text
design
pre_commit
pull_request
build
main
release
production
scheduled
exception
```

Example lifecycle:

```text
Requirement
    ↓
Design
    ↓
Local Verification
    ↓
Pull Request
    ↓
Automated Controls
    ↓
Review Controls
    ↓
Merge
    ↓
Release Controls
    ↓
Approval
    ↓
Production
```

Not every control runs at every stage.

## Automated Controls

Automated controls should be preferred when a requirement can be verified objectively and reliably.

Examples:

```text
Code must build
    ↓
ENG-001 Build Verification

Tests must pass
    ↓
TST-001 Automated Test Execution

Secrets must not be committed
    ↓
SEC-001 Secret Detection
```

Automation should reduce repeated human judgement, not create false confidence.

A weak or unreliable automated check should not replace necessary engineering review.

## Review Controls

Some requirements require judgement.

Examples include:

- whether architecture is unnecessarily complex
- whether a test strategy is sufficient
- whether a security design introduces unacceptable risk
- whether a system is operationally ready

These controls should produce explicit review outcomes.

Example:

```text
ARC-002 Architecture Review
        ↓
APPROVE
APPROVE WITH CONDITIONS
REWORK REQUIRED
INSUFFICIENT INFORMATION
```

The review outcome can then be mapped into common control evidence.

## Approval Controls

Approval controls are used when explicit authority is required.

They apply to activities such as:

- production deployment
- destructive production operations
- quality-gate exceptions
- breaking contract changes
- material security-policy changes

Approval requirements are defined by:

```text
policies/human-approval.md
```

Technical ability to perform an operation does not count as approval.

## Preventive Controls

Preventive controls stop prohibited actions before they occur.

Examples include:

- branch protection
- protected environments
- role-based access controls
- deployment permissions
- mandatory CI status checks

Where practical, high-risk requirements should use preventive controls rather than relying solely on written instructions.

## Control Exceptions

Blocking controls must not be bypassed silently.

Exceptions must follow:

```text
policies/quality-gates.md
policies/human-approval.md
```

An authorised exception should record:

- control ID
- reason
- risk
- scope
- approver
- expiry where appropriate
- remediation plan where applicable

The exception itself must produce governance evidence.

## Controls and AI Agents

AI agents may:

- inspect standards and policies
- determine which controls apply
- invoke controls through approved tools
- inspect evidence
- explain failures
- recommend remediation

AI agents must not:

- treat instructions as proof of compliance
- claim a control passed when it was not executed
- fabricate evidence
- silently bypass a blocking control
- independently approve high-risk actions
- weaken required controls for convenience

Agents operate within the control system, not above it.

## Separation of Organisational Control and Tooling

The platform deliberately separates a control from its implementation.

For example:

```text
SEC-001 Secret Detection
```

is durable.

Possible implementations include:

```text
Gitleaks
GitHub Secret Scanning
another approved tool
```

Similarly:

```text
SEC-003 Static Application Security Testing
```

might be implemented using different scanners over time.

Changing the tool should not require redefining the organisational requirement.

## Portability

Controls should remain portable across:

- GitHub Actions
- Azure DevOps
- GitLab CI
- other CI systems
- GitHub Copilot
- Claude Code
- Codex
- future engineering agents

Tool-specific adapters may implement controls, but organisational control definitions should remain vendor-neutral where practical.

## Control Evolution

When recurring engineering problems occur:

1. identify the underlying requirement
2. determine whether a relevant standard or policy already exists
3. determine whether an existing control should be strengthened
4. create a new control only when necessary
5. automate the control where reliable verification is possible
6. define the required evidence
7. evaluate whether the control reduces recurrence

Do not create controls merely to increase the number of quality gates.

Each control should address a meaningful engineering, security, operational, or governance risk.

## Phase 0 Initial Controls

Phase 0 initially implements a small set of high-value controls:

```text
ENG-001  Build Verification
ENG-003  Formatting / Linting
TST-001  Automated Test Execution
SEC-001  Secret Detection
SEC-002  Dependency Vulnerability Scan
```

These establish the first executable platform flow:

```text
Standards / Policies
        ↓
Control Catalogue
        ↓
CI Execution
        ↓
Evidence
        ↓
Quality Gate
```

Additional controls should be introduced incrementally based on real engineering needs discovered while building prototype systems.

## Related Files

```text
AGENTS.md

controls/
├── README.md
├── control-matrix.md
└── catalog.yaml

evidence/
├── README.md
├── evidence-contract.md
└── schema/
    └── control-evidence.schema.json

policies/
├── human-approval.md
├── quality-gates.md
└── secrets.md

standards/
├── architecture/
├── engineering/
├── testing/
├── security/
├── api/
├── observability/
└── ai/
```

## Architectural Principle

The control framework should preserve the separation:

```text
Organisational Intent
        ↓
Standards / Policies
        ↓
Stable Control Definition
        ↓
Tool-Specific Implementation
        ↓
Evidence
        ↓
Decision
```

Standards and control identities should be durable.

Tools and agents are replaceable.

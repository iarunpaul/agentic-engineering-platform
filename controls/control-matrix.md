# Engineering Control Matrix

## Purpose

Map organisational standards and policies to verification controls, enforcement points and evidence.

This document provides a human-readable view.

The machine-readable source is:

```text
controls/catalog.yaml
```

## Control Model

```text
Requirement
    ↓
Control
    ↓
Execution
    ↓
Gate
    ↓
Evidence
```

---

## Engineering Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| ENG-001 | Software must compile/build successfully | Engineering Standard | Build verification | Automated | Blocking | Build result |
| ENG-002 | Code must meet repository static-quality rules | Engineering Standard | Static analysis | Automated | Blocking | Analyzer report |
| ENG-003 | Formatting/linting rules must be satisfied | Engineering Standard | Formatting/lint check | Automated | Blocking | Lint result |
| ENG-004 | Material contract changes must consider compatibility | Engineering Standard | Compatibility review | Review | Conditional | Review decision |
| ENG-005 | New dependencies must be intentional and controlled | Engineering Standard | Dependency review | Automated + Review | Conditional | Dependency diff / review |

---

## Testing Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| TST-001 | Automated tests must pass | Testing Standard | Test execution | Automated | Blocking | Test report |
| TST-002 | Relevant behaviour must have appropriate verification | Testing Standard | Test adequacy review | Review | Conditional | Test review |
| TST-003 | External contracts should be verified where applicable | Testing Standard | Contract testing | Automated | Conditional | Contract test result |
| TST-004 | Flaky tests must not be silently accepted | Testing Standard | Flaky-test detection/review | Automated + Review | Conditional | Test history / exception |
| TST-005 | Security-sensitive behaviour must be tested | Testing Standard | Security behaviour tests | Automated | Conditional | Test report |

---

## Security Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| SEC-001 | Secrets must not be committed | Secrets Policy | Secret scanning | Automated | Blocking | Scanner report |
| SEC-002 | Dependencies must be checked for known vulnerabilities | Secure Engineering Standard | Dependency vulnerability scanning | Automated | Blocking by severity | Vulnerability report |
| SEC-003 | Source code should be checked for security weaknesses | Secure Engineering Standard | SAST | Automated | Blocking by severity | SAST report |
| SEC-004 | Infrastructure definitions should be security scanned | Secure Engineering Standard | IaC scanning | Automated | Conditional | IaC scan report |
| SEC-005 | Container images should be vulnerability scanned | Secure Engineering Standard | Container scanning | Automated | Conditional | Container scan |
| SEC-006 | Security-sensitive changes require security review | Secure Engineering Standard | Security review | Review | Conditional | Security-review decision |
| SEC-007 | Tenant boundaries must be protected | Secure Engineering Standard | Tenant isolation verification | Automated + Review | Conditional | Tests / review evidence |
| SEC-008 | Exposed secrets must be rotated | Secrets Policy | Secret exposure response | Approval + Review | Blocking | Rotation evidence |
| SEC-009 | GitHub Actions must use immutable full commit SHAs | Secure Engineering Standard + Quality Gates Policy | Action pinning validation | Automated + Preventive | Blocking | Workflow supply-chain validation |

---

## API Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| API-001 | API contracts must be valid | API Standard | Contract/schema validation | Automated | Blocking | Validation report |
| API-002 | Breaking contract changes must be identified | API Standard | Compatibility detection | Automated | Conditional | Compatibility report |
| API-003 | Breaking changes require explicit approval | API Standard + Human Approval Policy | Breaking-change approval | Approval | Blocking | Approval record |
| API-004 | API definitions should follow governance rules | API Standard | API linting | Automated | Conditional | Lint report |

---

## Architecture Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| ARC-001 | Material architecture changes must be challenged before implementation | Architecture Principles | Grill review | Review | Conditional | Grill outcome |
| ARC-002 | Significant architecture must comply with organisational principles | Architecture Principles | Architecture review | Review | Conditional | Architecture review |
| ARC-003 | Consequential decisions must be recorded | Architecture Principles | ADR presence check | Review | Conditional | ADR reference |
| ARC-004 | Architecture should avoid unjustified complexity | Architecture Principles | Complexity review | Review | Conditional | Architecture decision |
| ARC-005 | Architectural constraints should be machine-verifiable where practical | Architecture Principles | Architecture tests | Automated | Conditional | Architecture test report |

---

## Observability Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| OBS-001 | Material systems must provide operational telemetry | Observability Standard | Observability review | Review | Conditional | Review decision |
| OBS-002 | Secrets and prohibited sensitive data must not be logged | Observability + Secrets Policy | Logging/security analysis | Automated + Review | Conditional | Scan/test result |
| OBS-003 | Production services require meaningful health signals | Observability Standard | Health-check verification | Automated | Conditional | Integration/deployment test |
| OBS-004 | Important distributed operations should support correlation | Observability Standard | Correlation verification | Automated + Review | Conditional | Test/review evidence |

---

## AI-Assisted Engineering Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| AI-001 | AI-generated changes must pass normal engineering controls | AI-Assisted Engineering Standard | Standard CI pipeline | Automated | Blocking | CI evidence |
| AI-002 | Agents must not claim unperformed verification | AI-Assisted Engineering Standard | Evidence-backed reporting | Review | Conditional | Agent output + CI evidence |
| AI-003 | Durable rules must not exist only in vendor prompts | Agent Portability Standard | Portability review | Review | Non-blocking | Review record |
| AI-004 | Vendor-specific integration must not override organisational policy | Agent Portability Standard | Configuration review | Review | Conditional | Review evidence |
| AI-005 | High-risk agent actions require explicit approval | AI-Assisted Engineering Standard + Human Approval Policy | Human approval gate | Approval | Blocking | Approval record |

---

## Production and Release Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| REL-001 | Production readiness must be evaluated for material releases | Production Readiness Skill | Production-readiness review | Review | Conditional | Readiness decision |
| REL-002 | Deployment mechanism must be repeatable | Engineering + Architecture Standards | Deployment validation | Automated | Conditional | Deployment test |
| REL-003 | Data migrations must be assessed for safety | Human Approval Policy + Engineering Standard | Migration review | Review | Conditional | Migration plan / result |
| REL-004 | Destructive production operations require approval | Human Approval Policy | Protected approval gate | Approval | Blocking | Approval record |
| REL-005 | Production deployment requires authorised release mechanism | Human Approval Policy | Protected environment | Preventive + Approval | Blocking | Deployment approval |

---

## Governance Controls

| ID | Requirement | Source | Control | Type | Enforcement | Evidence |
|---|---|---|---|---|---|---|
| GOV-001 | Required quality gates must not be bypassed silently | Quality Gates Policy | Branch / pipeline protection | Preventive | Blocking | Platform configuration |
| GOV-002 | Control exceptions require explicit approval | Quality Gates Policy | Exception approval | Approval | Blocking | Exception record |
| GOV-003 | Control evidence must reflect actual execution | Quality Gates Policy | Evidence validation | Automated | Blocking | Evidence artifact |
| GOV-004 | Production or security governance changes require approval | Human Approval Policy | Governance approval | Approval | Blocking | Approval record |

---

## Control Execution Stages

Controls should run as early as practical.

```text
Developer / Agent
        │
        ▼
Local Verification
        │
        ▼
Pull Request
        │
        ├── Build
        ├── Lint
        ├── Tests
        ├── Secret Scan
        ├── Dependency Scan
        ├── SAST
        └── Contract Validation
        │
        ▼
Review Gates
        │
        ├── Architecture Review
        ├── Security Review
        └── Test Adequacy Review
        │
        ▼
Merge
        │
        ▼
Release Verification
        │
        ├── Artifact Verification
        ├── Deployment Validation
        ├── Production Readiness
        └── Human Approval
        │
        ▼
Production
```

## Control Timing Principle

Run controls as early as practical, but avoid unnecessary cost.

Prefer cheap and fast controls before expensive controls.

Example:

```text
format / lint
      ↓
build
      ↓
unit tests
      ↓
secret scan
      ↓
dependency scan
      ↓
SAST
      ↓
integration tests
      ↓
contract tests
      ↓
deployment validation
```

Actual ordering may vary by repository, technology and execution cost.

---

## Enforcement Levels

Controls use one of the following enforcement levels.

### Blocking

A failed control prevents the protected transition.

Examples include:

- merge
- release
- deployment

### Non-Blocking

The result provides engineering information but does not automatically prevent progression.

Non-blocking controls should still be reviewed where they identify meaningful risk.

### Conditional

The control applies only when relevant conditions are met.

Conditions may include:

- affected component
- change type
- environment
- technology
- architecture impact
- security impact
- risk classification

Conditional controls should not be silently skipped.

Where a normally applicable control is marked `NOT_APPLICABLE`, the reason should be recorded.

---

## Control Outcomes

Controls should use the common evidence outcomes:

```text
PASS
FAIL
WARN
NOT_APPLICABLE
NOT_EXECUTED
```

### PASS

The control was executed and satisfied its acceptance criteria.

### FAIL

The control was executed and did not satisfy its acceptance criteria.

### WARN

The control found an issue that does not automatically block progression.

### NOT_APPLICABLE

The control does not apply to the evaluated change.

### NOT_EXECUTED

The control applies but was not executed.

`NOT_EXECUTED` must never be interpreted as `PASS`.

---

## Evidence Model

Each control should produce or reference evidence.

Evidence should conform to the repository evidence model under:

```text
evidence/
```

Examples include:

```text
ENG-001
    ↓
CI build execution
    ↓
build result
    ↓
PASS

TST-001
    ↓
test runner
    ↓
machine-readable test report
    ↓
PASS

SEC-001
    ↓
secret scanner
    ↓
scanner report
    ↓
PASS

ARC-002
    ↓
architecture-review skill + human review where required
    ↓
architecture review decision
    ↓
PASS / FAIL / WARN
```

A statement from an agent that a control "looks fine" is not equivalent to control evidence unless the required verification was actually performed.

---

## Relationship Between Standards, Policies and Controls

Standards describe expected engineering practice.

Policies define mandatory constraints.

Controls verify or enforce those requirements.

Example:

```text
standards/testing/testing-standard.md
        ↓
Automated tests must provide appropriate behavioural evidence
        ↓
TST-001 Automated Test Execution
        ↓
CI test runner
        ↓
Test report
```

Example:

```text
policies/secrets.md
        ↓
Secrets must not be committed
        ↓
SEC-001 Secret Detection
        ↓
Secret scanner
        ↓
Scanner report
```

Example:

```text
policies/human-approval.md
        ↓
Production deployment requires authorised human approval
        ↓
REL-005 Production Deployment Approval
        ↓
Protected production environment
        ↓
Approval record
```

---

## Guidance Versus Enforcement

Not every engineering expectation can or should be converted into an automated control.

For example:

```text
Architecture should avoid unnecessary complexity
```

requires engineering judgement.

It maps to:

```text
ARC-004 Complexity Review
```

rather than a simplistic automated rule.

In contrast:

```text
Secrets must not be committed
```

can be objectively checked and should therefore use automated enforcement.

The preferred hierarchy is:

```text
Objective rule
    ↓
Automated control where reliable

Judgement-based rule
    ↓
Review control

High-risk action
    ↓
Human approval or preventive control
```

---

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
- approver
- scope
- expiry where appropriate
- remediation plan where applicable

The exception itself becomes governance evidence.

---

## Control Ownership and Evolution

Each control should have a stable organisational identity independent of its implementation tool.

For example:

```text
SEC-001 Secret Detection
```

is the durable control.

Its implementation might initially be:

```text
Gitleaks
```

and later become:

```text
GitHub Secret Scanning
```

without changing the organisational control ID.

Controls should evolve when:

- recurring defects expose missing verification
- new security risks emerge
- technology changes
- organisational policy changes
- regulatory requirements change
- existing controls create excessive false positives
- automation can replace repeated manual review

Do not add controls merely to increase the number of gates.

Every control should address a meaningful engineering or governance risk.

---

## Machine-Readable Catalogue

The human-readable matrix in this document should remain aligned with:

```text
controls/catalog.yaml
```

The catalogue is intended to become the machine-readable source used by:

- CI pipelines
- control-validation scripts
- evidence collectors
- reporting
- future agent tooling

Changes to control IDs, enforcement behaviour or evidence expectations should update both representations until automated generation or validation removes the need for manual synchronisation.

---

## Phase 0 Initial Enforcement

Phase 0 should initially implement a small set of real automated controls:

```text
ENG-001  Build Verification
ENG-003  Formatting / Linting
TST-001  Automated Test Execution
SEC-001  Secret Detection
SEC-002  Dependency Vulnerability Scan
```

These controls establish the first executable flow:

```text
Standards / Policies
        ↓
Control Catalogue
        ↓
CI Execution
        ↓
Evidence
        ↓
Blocking Gate
```

Additional controls should be introduced incrementally as the platform and prototype projects provide real requirements.

## Architectural Principle

The control framework should remain portable.

Organisational controls must not depend on a particular:

- AI agent
- IDE
- CI vendor
- security scanner
- cloud provider

Tool-specific implementations may change.

The organisational requirement, control identity and evidence expectation should remain stable wherever practical.

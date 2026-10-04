# Engineering Evidence

## Purpose

The `evidence/` directory defines how the platform proves that engineering controls were actually evaluated.

Evidence provides traceability between:

```text
Requirement
    ↓
Control
    ↓
Execution
    ↓
Result
```

The evidence layer allows the platform to distinguish between:

- expected behaviour
- attempted verification
- successful verification
- failed verification
- missing verification
- approved exceptions

## Core Principle

> No evidence means no verified control outcome.

Statements such as:

```text
"The tests should pass."
```

or:

```text
"Security looks fine."
```

are not control evidence.

Evidence must come from an actual execution, review, approval, or other defined control mechanism.

## Evidence Sources

Evidence may originate from:

- local development tools
- CI pipelines
- test frameworks
- security scanners
- dependency scanners
- static-analysis tools
- infrastructure scanners
- deployment systems
- architecture reviews
- security reviews
- production-readiness reviews
- human approval systems
- AI-agent-assisted reviews

The source must accurately reflect how the evidence was produced.

## Evidence Types

Examples include:

```text
build-result
lint-result
static-analysis-report
test-report
contract-validation-report
compatibility-report
security-scan-report
vulnerability-report
sast-report
iac-security-report
container-scan-report
architecture-review
security-review
observability-review
production-readiness-review
approval-record
deployment-result
exception-record
governance-configuration
evidence-validation-result
```

The evidence type should describe what was verified, not the vendor or tool used.

For example:

```text
security-scan-report
```

is preferable to:

```text
gitleaks-report
```

at the organisational evidence-contract level.

Tool-specific information can be recorded separately.

## Evidence Outcomes

Controls should use the common outcomes:

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

The control found an issue that requires attention but does not automatically block progression.

### NOT_APPLICABLE

The control does not apply to the evaluated subject.

Where a control would normally be expected, the reason should be recorded.

### NOT_EXECUTED

The control applies but was not executed.

`NOT_EXECUTED` must never be interpreted as `PASS`.

## Evidence Properties

Every material evidence record should identify:

- control ID
- timestamp
- result
- subject being evaluated
- source
- relevant repository where applicable
- commit or artifact identifier where applicable
- execution context
- tool where applicable
- location of detailed evidence where applicable

## Evidence Subject

Evidence must identify what was evaluated.

Examples include:

```text
commit
pull-request
build
artifact
container-image
architecture-change
deployment
release
production-change
```

Example:

```text
control: TST-001
subject: commit a83de1f
status: PASS
```

This prevents evidence from being detached from the change it actually validated.

## Evidence Integrity

Evidence should be produced as close as practical to the system performing the verification.

Preferred:

```text
CI test runner
    ↓
machine-readable test result
    ↓
control evidence
```

Less preferred:

```text
AI agent
    ↓
"Tests passed"
```

An agent statement is acceptable only when backed by real tool execution or a referenced authoritative result.

## Evidence and AI Agents

Agents may:

- execute approved controls
- inspect evidence
- aggregate evidence
- summarise results
- identify missing evidence
- recommend remediation

Agents must not:

- fabricate evidence
- infer `PASS` from absence of failure
- convert `NOT_EXECUTED` to `PASS`
- hide failed controls
- claim stronger assurance than the evidence supports
- approve high-risk actions unless explicitly authorised by policy

Agents should distinguish clearly between:

```text
VERIFIED
INFERRED
RECOMMENDED
NOT_EXECUTED
```

## Machine-Readable Evidence

The logical evidence contract is defined in:

```text
evidence/evidence-contract.md
```

The machine-readable schema is defined in:

```text
evidence/schema/control-evidence.schema.json
```

Control evidence intended for automation should conform to that schema where practical.

## Evidence Example

A successful test control might produce:

```json
{
  "controlId": "TST-001",
  "timestamp": "2026-10-03T00:30:00Z",
  "status": "PASS",
  "subject": {
    "type": "commit",
    "value": "a83de1f"
  },
  "source": "ci",
  "repository": "agentic-engineering-platform",
  "commit": "a83de1f",
  "runId": "18452",
  "tool": "dotnet-test",
  "summary": "All automated tests passed.",
  "metadata": {
    "total": 184,
    "passed": 184,
    "failed": 0
  }
}
```

The control remains:

```text
TST-001 Automated Test Execution
```

even if the underlying test framework later changes.

## Review Evidence

Controls requiring engineering judgement should also produce evidence.

Example:

```text
ARC-002 Architecture Review
        ↓
architecture review performed
        ↓
APPROVE WITH CONDITIONS
        ↓
review evidence
```

Review evidence should capture:

- control ID
- subject
- decision
- material findings
- reviewer or review mechanism where appropriate
- timestamp
- remaining conditions

The evidence should not attempt to preserve every discussion.

It should preserve the decision and material reasoning needed for traceability.

## Approval Evidence

Human approval controls must produce an explicit approval record.

Example:

```text
REL-005 Production Deployment Approval
        ↓
authorised human approval
        ↓
approval evidence
```

Approval evidence should identify:

- control
- action approved
- scope
- approver
- timestamp
- environment where relevant
- conditions where applicable

Do not infer approval from repository permissions or tool access.

## Exception Evidence

A control exception is itself a governed event.

An exception record should capture:

- affected control ID
- reason
- risk
- scope
- approver
- timestamp
- expiry where applicable
- remediation action where applicable

Example:

```text
GOV-002 Quality Gate Exception Approval
        ↓
approved temporary exception
        ↓
exception evidence
```

An exception does not convert the underlying control into a successful execution.

For example:

```text
SEC-003 = FAIL
GOV-002 = PASS
```

may permit progression under an approved exception.

It must not be rewritten as:

```text
SEC-003 = PASS
```

## Evidence Aggregation

A release or merge decision may depend on evidence from multiple controls.

Example:

```text
ENG-001 Build                         PASS
ENG-003 Lint                          PASS
TST-001 Tests                         PASS
SEC-001 Secret Scan                   PASS
SEC-002 Dependency Scan               PASS
SEC-003 SAST                          PASS
ARC-002 Architecture Review           PASS
REL-001 Production Readiness          PASS
REL-005 Deployment Approval           PASS
                                      ↓
                                RELEASE ALLOWED
```

If a required blocking control fails:

```text
SEC-001 Secret Scan                   FAIL
                                      ↓
                                RELEASE BLOCKED
```

unless a valid authorised exception mechanism exists.

## Evidence Validation

Evidence itself should be validated.

The governance control:

```text
GOV-003 Evidence Validation
```

exists to ensure that evidence:

- uses recognised control IDs
- has valid outcomes
- references the correct subject
- conforms to the evidence schema where required
- is not missing required fields
- is not reported as PASS without execution

This allows the platform to treat evidence as structured engineering data rather than arbitrary text.

## Evidence Storage

Phase 0 does not require a central evidence database.

Evidence may initially exist as:

- CI job results
- workflow artifacts
- test reports
- scanner outputs
- pull-request checks
- review records
- deployment approvals
- environment protection records

The common contract makes later aggregation possible without forcing a central platform too early.

## Evidence Retention

Retention should be proportionate to risk and organisational requirements.

Short-lived development evidence may have limited retention.

Longer retention may be appropriate for:

- production releases
- security reviews
- production approvals
- high-risk migrations
- regulatory controls
- approved exceptions
- incident-related changes

Retention requirements should be defined by organisational policy when needed.

## Evidence Immutability

Where evidence supports consequential release or governance decisions, it should be difficult to silently alter after the fact.

Prefer evidence produced and retained by trusted systems such as:

- CI platforms
- deployment systems
- protected approval workflows
- security tooling

Do not rely solely on manually editable local files for high-risk governance evidence.

## Evidence Location

Evidence records may reference detailed artifacts using an `evidenceUri` or equivalent location.

Examples include:

```text
CI artifact
test report
scanner report
pull-request review
deployment record
approval record
```

The evidence record itself should remain meaningful even if detailed artifacts later expire.

## Evidence and Tool Independence

Evidence contracts should remain portable across tools.

For example:

```text
SEC-001 Secret Detection
        ↓
security-scan-report
```

might initially be generated by:

```text
Gitleaks
```

and later by:

```text
GitHub Secret Scanning
```

The organisational control and evidence type do not need to change.

Tool-specific details belong in fields such as:

```text
tool
toolVersion
metadata
```

## Evidence and CI Vendors

The evidence model should remain usable across:

- GitHub Actions
- Azure DevOps
- GitLab CI
- Jenkins
- other CI/CD systems

The CI system is an evidence producer, not the owner of the organisational control model.

## Evidence Flow

The intended platform flow is:

```text
Standard / Policy
        ↓
Control Definition
        ↓
Control Execution
        ↓
Evidence Produced
        ↓
Evidence Validated
        ↓
Gate Decision
        ↓
Merge / Release / Block
```

## Phase 0 Evidence Scope

Phase 0 should initially produce evidence for:

```text
ENG-001  Build Verification
ENG-003  Formatting / Linting
TST-001  Automated Test Execution
SEC-001  Secret Detection
SEC-002  Dependency Vulnerability Scan
```

Example:

```text
Pull Request
    │
    ├── ENG-001 → build evidence
    ├── ENG-003 → lint evidence
    ├── TST-001 → test evidence
    ├── SEC-001 → secret-scan evidence
    └── SEC-002 → vulnerability evidence
            │
            ▼
      evidence validation
            │
            ▼
       quality gate
```

This gives the platform its first auditable:

```text
Standards
    ↓
Controls
    ↓
Evidence
    ↓
Decision
```

workflow.

## Related Files

```text
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
```

## Architectural Principle

The evidence layer exists to answer:

> What objective or reviewable proof do we have that this requirement was actually checked?

The platform should never confuse:

```text
instruction
```

with:

```text
verification
```

or:

```text
verification
```

with:

```text
evidence
```

The intended separation is:

```text
Guidance
    ↓
Control
    ↓
Execution
    ↓
Evidence
    ↓
Decision
```

That separation is fundamental to trustworthy agentic engineering.

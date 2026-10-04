# CI Workflow Foundation

## Purpose

Define the CI execution layer for the Agentic Engineering Platform.

CI turns organisational controls into repeatable, enforceable engineering gates.

The intended flow is:

```text
Standards / Policies
        ↓
Control Catalogue
        ↓
Portable Scripts
        ↓
CI Workflow
        ↓
Control Execution
        ↓
Evidence
        ↓
Gate Decision
```

## Core Principle

> CI enforces controls; it does not define organisational policy.

Organisational requirements belong in:

```text
standards/
policies/
controls/
```

Vendor-specific workflow configuration should implement those requirements rather than becoming their authoritative source.

## Phase 0 Controls

The initial CI workflow should implement:

```text
ENG-001  Build Verification
ENG-003  Formatting / Linting
TST-001  Automated Test Execution
SEC-001  Secret Detection
SEC-002  Dependency Vulnerability Scan
```

These controls provide the first executable quality gate.

## Expected Flow

```text
Pull Request
      │
      ├── ENG-003 Formatting / Lint
      │
      ├── ENG-001 Build
      │
      ├── TST-001 Tests
      │
      ├── SEC-001 Secret Scan
      │
      └── SEC-002 Dependency Scan
               │
               ▼
        Evidence Generation
               │
               ▼
        Evidence Validation
               │
               ▼
          Quality Gate
           /        \
         PASS       FAIL
          │           │
        Merge        Block
```

## Fail Fast

Cheap, deterministic checks should generally run before expensive verification.

A typical ordering is:

```text
configuration validation
        ↓
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
more expensive controls
```

Parallel execution may be used where it improves feedback time without weakening dependencies between controls.

## Evidence

Each control execution should create or reference evidence compatible with:

```text
evidence/evidence-contract.md
```

CI should eventually aggregate evidence into a machine-readable control result.

CI status alone should not become the only evidence representation.

## Portability

Portable engineering logic should preferably exist outside vendor-specific workflow files.

For example:

```text
scripts/
```

may contain reusable control execution logic.

GitHub Actions, Azure DevOps or another CI platform should invoke that logic.

This allows:

```text
GitHub Actions
Azure DevOps
GitLab CI
local agent execution
```

to perform equivalent verification.

## Blocking Controls

Required Phase 0 controls should block merge when they fail.

Agents must not automatically modify CI configuration to bypass a failure.

Failures should be:

1. diagnosed
2. corrected
3. rerun

If an exception is genuinely required, it must follow:

```text
policies/quality-gates.md
policies/human-approval.md
```

## Pull Requests

Pull-request CI should provide fast engineering feedback.

At minimum Phase 0 should eventually verify:

- repository structure
- formatting
- build
- tests
- secrets
- vulnerable dependencies

Future projects may add:

- SAST
- API compatibility
- architecture tests
- IaC scanning
- container scanning
- integration tests

## Main Branch

The main branch should remain in a releasable or clearly understood state.

Controls required for pull requests should also protect direct changes to main where the hosting platform supports this.

## Release

Release workflows may introduce additional controls such as:

```text
REL-001 Production Readiness
REL-002 Deployment Validation
REL-005 Production Deployment Approval
```

Phase 0 does not need to implement the complete production-release lifecycle immediately.

## CI Vendor Separation

GitHub-specific workflows should eventually live under:

```text
.github/workflows/
```

Organisational CI architecture should remain independent of GitHub.

A future structure may therefore become:

```text
ci/
    README.md

scripts/
    run-quality-gates
    collect-evidence

.github/workflows/
    pull-request.yml
    release.yml
```

This preserves:

```text
Organisation rules
      ↓
portable execution
      ↓
vendor adapter
```

rather than:

```text
GitHub YAML
      ↓
organisation rules
```

## Evolution

Additional controls should be introduced because real engineering risk requires them.

Do not activate every possible security or quality scanner merely to make the pipeline appear comprehensive.

Controls should provide meaningful assurance while maintaining useful engineering feedback times.

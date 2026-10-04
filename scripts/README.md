# Platform Scripts

## Purpose

The `scripts/` directory contains portable automation used by developers, AI agents and CI pipelines.

Scripts convert engineering expectations into repeatable executable behaviour.

Examples include:

- control execution
- control validation
- evidence generation
- evidence validation
- repository validation
- local quality checks

## Core Principle

> If an engineering activity is deterministic and repeatedly performed, prefer automation over repeated manual instructions.

## Script Responsibilities

Scripts may:

- execute controls
- normalise tool output
- generate evidence
- validate configuration
- validate control catalogues
- validate evidence schemas
- aggregate control results

Scripts should not silently redefine organisational policy.

The authoritative sources remain:

```text
standards/
policies/
controls/
```

## Portability

Scripts should remain portable where practical.

Avoid unnecessary coupling to:

- GitHub Actions
- Azure DevOps
- a specific AI agent
- a developer's local machine configuration

CI workflows should preferably call reusable scripts rather than duplicate engineering logic directly inside vendor-specific workflow definitions.

Preferred:

```text
CI workflow
    ↓
scripts/run-quality-gates
    ↓
control tooling
```

Avoid:

```text
GitHub-specific workflow
    ↓
all engineering logic embedded directly in YAML
```

## Expected Phase 0 Scripts

Phase 0 is expected to introduce scripts such as:

```text
validate-control-catalog
validate-evidence
run-quality-gates
collect-evidence
```

Exact implementation languages should be selected based on portability and maintainability.

Do not create custom tooling where established tools already solve the problem reliably.

## Exit Codes

Scripts used by CI should use predictable exit codes.

Typically:

```text
0 = success
non-zero = failure
```

Where more detailed results are required, produce structured output rather than encoding complex semantics into exit codes.

## Output

Scripts intended for automation should prefer:

- deterministic output
- machine-readable artifacts
- clear error messages

Avoid depending on parsing human-oriented console text when structured output is available.

## Evidence

Scripts executing organisational controls should create or reference evidence conforming to:

```text
evidence/evidence-contract.md
```

## Security

Scripts must follow organisational security standards.

They must not:

- print secrets
- embed production credentials
- bypass approval controls
- disable quality gates
- silently ignore failed commands

## AI Agents

Agents may invoke approved scripts.

Agents should prefer existing repository automation over recreating the same verification manually.

If an existing script fails, the agent must report the failure rather than bypassing it.

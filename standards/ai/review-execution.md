# Review Execution Standard

## Purpose

Define common execution semantics for AI-assisted engineering reviews.

This standard applies to review workflows such as:

- Grill
- architecture review
- security review
- production-readiness review
- other future engineering review skills

The reasoning performed by a review may be probabilistic.

The execution envelope around that reasoning must be as deterministic, repeatable and auditable as practical.

## Core Principle

> Review reasoning may vary; review inputs, identity, evidence and persistence must not be ambiguous.

## 1. Explicit Review Target

Every review must have an explicit target.

Examples:

```text
requirements document
ADR
architecture document
implementation plan
production change plan
source-code change
```

If the user explicitly supplies a target, use it.

If no target is supplied:

1. inspect candidate artifacts
2. if exactly one credible active target exists, state it before proceeding
3. if multiple credible targets exist, ask the user to choose
4. do not silently perform a repository-wide review

Repository-wide review is a separate explicit mode.

## 2. Review Context

A review target must not be evaluated in isolation where relevant upstream evidence exists.

Resolve only context materially relevant to the target.

Typical context includes:

```text
requirements
    ↓
requirement review / Grill
    ↓
parent decisions
    ↓
previous reviews
    ↓
current review target
    ↓
applicable standards and policies
```

Do not load unrelated repository documents merely because they exist.

## 3. Context Precedence

Prefer context in this order:

1. explicit user-supplied context
2. artifact references contained in the review target
3. directly related upstream review artifacts
4. directly related parent ADRs or decisions
5. project requirements
6. applicable standards and policies

## 4. Review Input Manifest

Before final review execution, establish an input manifest containing:

```text
review type
skill
target path
target content hash
context paths
context content hashes
platform version
protocol version
```

Context paths must be sorted deterministically before fingerprinting.

## 5. Input Fingerprint

A review fingerprint must be derived from the normalized input manifest.

The fingerprint identifies the material evidence against which the review was performed.

It must not depend on:

- file modification timestamps
- local absolute paths
- chat session identifiers
- model-generated prose
- sequence numbers

The same normalized review inputs must produce the same fingerprint.

## 6. Idempotency

Before executing or persisting a completed review:

1. compute the review input fingerprint
2. inspect completed reviews of the same review category
3. determine whether an existing review has the same fingerprint

If an equivalent completed review exists:

```text
do not create a duplicate completed review
```

Instead, report the existing review.

A new review may be forced only when explicitly requested.

## 7. Reruns

A rerun against unchanged inputs is a deliberate new assessment.

It must be explicitly requested.

A forced rerun must:

- retain the same input fingerprint
- receive a new review ID
- reference the previous equivalent review
- record that it is a deliberate rerun

Example:

```yaml
rerun-of: REVIEW-ARC-0002
```

Do not silently replace the previous review.

## 8. Changed Inputs

If the target or material context changes, the fingerprint changes.

The resulting review is a new review.

Where appropriate it should record:

```yaml
supersedes: REVIEW-ARC-0002
```

Completed review history must not be silently overwritten.

## 9. Sequence Allocation

Review sequence numbers are scoped to the review category.

Examples:

```text
docs/reviews/requirements/
docs/reviews/architecture/
docs/reviews/implementation/
docs/reviews/security/
docs/reviews/production-readiness/
```

Allocate:

```text
max(existing sequence) + 1
```

Sequence allocation is an identifier concern.

It must not affect the input fingerprint.

## 10. Stable Review Metadata

Completed review artifacts should record:

```yaml
id:
type:
skill:
status:
date:
reviewed-artifact:
platform-version:
protocol-version:
input-fingerprint:
```

Where available also record:

```yaml
target-sha256:
context:
rerun-of:
supersedes:
```

## 11. Review Outcome Consistency

Repeated model reasoning is not guaranteed to generate byte-identical prose.

Consistency must therefore be established through:

- stable target selection
- stable context resolution
- stable severity vocabulary
- stable recommendation vocabulary
- fixed output schema
- explicit evidence references

Material outcome changes across forced reruns should remain visible rather than being hidden.

## 12. Immutable Completed Reviews

A completed review used as engineering evidence should be treated as immutable history.

If the reviewed artifact changes materially:

```text
create a new review
```

Do not rewrite the old review to make it appear to have reviewed later evidence.

Corrections to metadata may be made only where they do not alter the substantive historical review outcome.

## 13. Incomplete Reviews

Interactive discovery or partially completed review activity must not be treated as completed evidence.

Drafts must use:

```yaml
status: draft
```

Drafts do not satisfy completed review controls.

## 14. Prior Finding Traceability

Where an upstream review produced findings relevant to the current target, the current review should classify each relevant inherited finding as:

```text
RESOLVES
PARTIALLY RESOLVES
DOES NOT RESOLVE
NOT APPLICABLE
```

Review workflows must not silently discard unresolved upstream findings.

## 15. Persistence

Completed reviews must use the applicable review template and repository review location.

The final persisted artifact must contain the fingerprint used for execution.

If the runtime cannot persist the artifact, it must not claim that persistence occurred.

## 16. Automation Boundary

Deterministic operations should be performed by repository tooling where practical.

Examples:

- file hashing
- normalized manifest generation
- fingerprint generation
- equivalent-review detection
- sequence allocation

AI agents should not manually reproduce deterministic bookkeeping when repository tooling exists.

## 17. Human Accountability

Review automation does not change approval authority.

A review recommendation is engineering evidence.

It is not permission to perform a high-risk action unless repository policy explicitly grants that authority.
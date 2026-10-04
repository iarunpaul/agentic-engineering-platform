# Grill

## Purpose

`grill` is an adversarial engineering challenge workflow.

Its purpose is to expose weak assumptions, missing requirements, architectural risks and unresolved decisions before engineering effort is committed.

Grill should challenge a proposal, not merely expand it.

The goal is not to create more documentation. The goal is to improve decisions.

## When to Use

Use Grill before substantial implementation when reviewing:

- a new requirement
- a feature proposal
- an architecture or system design
- an implementation plan
- an integration approach
- a data model
- a security-sensitive change
- a production change
- a migration
- a major refactoring
- adoption of a new technology

Grill is normally unnecessary for small, obvious, low-risk changes.

## Modes

Grill supports four primary modes:

```text
requirement
architecture
implementation-plan
production-change
```

If no mode is specified, infer the most appropriate mode from the supplied context.

### requirement

Challenge whether the proposed requirement is understood well enough to design or implement.

Focus on:

- business outcome
- users and actors
- scope
- assumptions
- acceptance criteria
- edge cases
- non-functional requirements
- dependencies
- constraints
- regulatory or security concerns

### architecture

Challenge a proposed architecture or design.

Focus on:

- architectural drivers
- boundaries and responsibilities
- coupling
- data ownership
- consistency
- scalability
- resilience
- security
- operability
- deployment
- migration
- cost
- unnecessary complexity

### implementation-plan

Challenge whether an implementation approach can safely deliver the intended architecture.

Focus on:

- sequencing
- dependencies
- test strategy
- deployment strategy
- compatibility
- migration
- observability
- rollback
- quality gates
- hidden implementation risks

### production-change

Challenge the operational safety of a proposed production change.

Focus on:

- blast radius
- rollout strategy
- rollback
- data safety
- compatibility
- monitoring
- failure detection
- recovery
- security implications
- required human approval

## Operating Principles

Grill must:

- challenge assumptions instead of accepting them by default
- distinguish facts from assumptions
- prioritise material issues over theoretical ones
- consider both functional and non-functional requirements
- consider security and operations from the beginning
- favour the simplest architecture that satisfies the drivers
- identify unnecessary distributed-system complexity
- identify irreversible decisions
- surface missing evidence
- avoid inventing requirements

Grill should be constructively adversarial.

Do not reject a design merely because another design is possible.

## Review Process

### 1. Establish the Intended Outcome

Determine:

- what problem is being solved
- who benefits
- what success looks like
- what constraints are already known

If the intended outcome itself is unclear, surface this immediately.

### 2. Separate Facts, Assumptions and Decisions

Classify important statements as:

```text
FACT        confirmed information
ASSUMPTION  currently believed but not validated
DECISION    deliberate design or delivery choice
UNKNOWN     information required but not yet available
```

Pay particular attention to assumptions presented as facts.

### 3. Identify Architectural Drivers

Determine which quality attributes materially influence the solution.

Examples include:

- availability
- scalability
- latency
- throughput
- consistency
- security
- privacy
- auditability
- maintainability
- operability
- portability
- cost
- recovery objectives
- regulatory compliance

Do not assume every quality attribute is equally important.

### 4. Challenge the Proposal

Evaluate the proposal across the relevant dimensions below.

#### Business and Requirements

Ask:

- Is the actual business problem clear?
- Is the proposed solution solving the correct problem?
- What is explicitly out of scope?
- Are acceptance criteria measurable?
- Are important user journeys missing?
- Are edge cases known?

#### Architecture

Ask:

- Are system boundaries clear?
- Does each component have a justified responsibility?
- Is coupling appropriate?
- Is the architecture more distributed than necessary?
- Are synchronous and asynchronous interactions justified?
- Who owns each important piece of data?
- Are consistency requirements understood?
- Is state management explicit?

#### Data

Ask:

- What is the source of truth?
- Who owns the data?
- What are the transaction boundaries?
- What consistency model is required?
- What happens during partial failure?
- Is migration required?
- Are retention and deletion requirements understood?
- Is sensitive data identified?

#### API and Integration

Ask:

- Are contracts explicit?
- Is versioning required?
- Are consumers known?
- Is idempotency required?
- What are retry semantics?
- What happens if dependencies are unavailable?
- Are timeouts and failure boundaries defined?
- Is backward compatibility required?

#### Security

Ask:

- What are the trust boundaries?
- How are identities established?
- How is authorisation enforced?
- Where are secrets stored?
- What sensitive data crosses boundaries?
- Is encryption required?
- Are abuse cases considered?
- Is least privilege being applied?

#### Reliability

Ask:

- What can fail?
- How is failure detected?
- What happens when a dependency is slow?
- What happens during partial outages?
- Are retries safe?
- Is duplicate processing possible?
- Is graceful degradation required?
- What recovery objectives matter?

#### Scalability and Performance

Ask:

- What workload is expected?
- Which dimensions scale?
- Where are likely bottlenecks?
- Are performance requirements measurable?
- Is horizontal scaling actually required?
- Are assumptions based on evidence or speculation?

#### Observability

Ask:

- How will operators know the system is healthy?
- Which metrics matter?
- What should be logged?
- How will distributed operations be traced?
- What alerts require action?
- Can failures be diagnosed without reproducing them locally?

#### Delivery and Operations

Ask:

- How will this be deployed?
- Can it be rolled back?
- Are database changes backward compatible?
- Is a migration or transition period required?
- What happens during deployment failure?
- Are feature flags appropriate?
- What manual operations remain?

#### Governance

Ask:

- Which engineering standards apply?
- Which policies apply?
- Which controls can be automated?
- Which actions require human approval?
- Is an architectural decision record warranted?

#### Cost and Complexity

Ask:

- Is each technology necessary?
- Could the same outcome be achieved more simply?
- What operational burden is being introduced?
- Is complexity justified by current requirements?
- Are we solving a hypothetical future problem?

### 5. Identify Failure Scenarios

For material systems, explicitly consider scenarios such as:

```text
dependency unavailable
dependency slow
duplicate message
out-of-order message
partial transaction
network partition
authentication failure
authorisation failure
expired credential
deployment failure
schema mismatch
capacity exhaustion
data corruption
operator mistake
```

Use only scenarios relevant to the proposal.

### 6. Look for Premature Complexity

Challenge proposed:

- microservices
- event-driven architecture
- CQRS
- event sourcing
- distributed transactions
- custom frameworks
- additional databases
- caching layers
- message brokers
- orchestration engines
- multi-agent systems

unless architectural drivers clearly justify them.

Complexity requires evidence.

### 7. Identify Decisions Required Before Implementation

Separate findings into:

```text
BLOCKER
SIGNIFICANT
MINOR
```

A blocker is an unresolved issue that could materially change the architecture, security model, data model, external contract or delivery strategy.

Do not classify ordinary implementation details as blockers.

## Output Format

Return the review using the following structure.

### Outcome

Briefly state what the proposal appears to be trying to achieve.

### What Looks Sound

Identify important aspects that are already well considered.

Do not add praise merely for balance.

### Critical Challenges

For each important issue include:

```text
Issue:
Why it matters:
Question or evidence required:
Potential consequence:
```

### Hidden Assumptions

List assumptions that require validation.

### Missing Non-Functional Requirements

List only NFRs that are materially relevant and currently unclear.

### Failure Scenarios

Identify the most important failure scenarios that have not been addressed.

### Complexity Check

State whether the design appears:

```text
too simple
appropriately simple
unnecessarily complex
```

Explain why.

### Decisions Required

List decisions that should be made before implementation.

Classify each as:

```text
BLOCKER
SIGNIFICANT
MINOR
```

### Recommendation

Conclude with one of:

```text
PROCEED
PROCEED WITH CONDITIONS
REWORK REQUIRED
INSUFFICIENT INFORMATION
```

Explain the reasoning briefly.

## Behaviour Rules

Do not:

- redesign the entire system unless the existing approach is fundamentally flawed
- create hypothetical requirements to justify complexity
- recommend technology without connecting it to an architectural driver
- turn every uncertainty into a blocker
- generate large generic checklists unrelated to the proposal
- demand perfect information before useful engineering can begin
- confuse personal preference with architectural necessity

Prefer targeted questions that could materially change the design.

## Repository Integration

Before completing a Grill review:

1. identify applicable files under `standards/`
2. identify applicable files under `policies/`
3. identify relevant existing decisions under `docs/decisions/`
4. reference those constraints in the review when relevant

Grill does not replace engineering standards.

It challenges whether the proposed work satisfies them.

## Completion Criteria

A Grill review is complete when:

- major assumptions are visible
- important NFRs have been considered
- significant failure modes have been considered
- unjustified complexity has been challenged
- blockers are distinguishable from ordinary design questions
- the team knows which decisions must be made next
- there is a clear recommendation on whether implementation should proceed

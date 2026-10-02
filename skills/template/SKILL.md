# <Skill Name>

## Purpose

Describe the engineering activity this skill performs.

State clearly what outcome it should produce.

## When to Use

Use this skill when:

- <scenario where this skill should be applied>
- <another relevant scenario>

Do not use this skill when:

- <scenario where another skill is more appropriate>
- <low-risk or irrelevant scenario>

## Inputs

The skill may consume:

- task or requirement
- relevant source code
- architecture context
- applicable standards
- applicable policies
- architectural decisions
- CI or test results
- operational information

Only require inputs that are materially relevant.

## Applicable Repository Guidance

Before execution:

1. inspect relevant files under `standards/`
2. inspect relevant files under `policies/`
3. inspect relevant decisions under `docs/decisions/`
4. identify task-specific requirements

Repository standards and policies take precedence over this skill.

## Workflow

### 1. Understand Context

Describe what must be established before performing the activity.

### 2. Analyse

Describe the specialised reasoning required.

### 3. Execute

Describe actions the agent may perform.

### 4. Verify

Describe how the result should be validated.

### 5. Report

Describe what should be returned to the user or calling workflow.

## Risk Handling

Classify important findings when useful:

```text
BLOCKER
SIGNIFICANT
MINOR
```

Do not escalate routine implementation choices unnecessarily.

## Output Format

Specify a predictable output structure.

Keep output focused on decisions and actions.

## Behaviour Rules

The skill must:

- follow repository standards and policies
- distinguish assumptions from facts
- surface material risk
- avoid unnecessary complexity
- avoid claiming verification that was not performed

The skill must not:

- override repository policy
- bypass quality gates
- invent requirements
- conceal failed validation
- perform high-risk actions without required approval

## Completion Criteria

The skill is complete when:

- its intended engineering outcome has been achieved
- material assumptions are explicit
- relevant risks are visible
- required validation has been performed or identified
- remaining actions are clear
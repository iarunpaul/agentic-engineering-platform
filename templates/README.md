# Engineering Templates

## Purpose

The `templates/` directory contains reusable structures for recurring engineering artifacts.

Templates improve consistency without forcing unnecessary documentation.

## Core Principle

> Standardise structure where consistency helps; avoid documentation for its own sake.

## Appropriate Templates

Examples may include:

- pull-request descriptions
- architecture reviews
- security reviews
- production-readiness reviews
- control exceptions
- incident summaries
- migration plans

Architecture Decision Records are maintained under:

```text
docs/decisions/
```

## Template Design

Templates should:

- be concise
- focus on engineering decisions and evidence
- avoid duplicate information already available from tooling
- distinguish required from optional content
- remain technology-neutral where practical

## AI Agents

Agents may use templates when producing engineering artifacts.

A template does not replace engineering judgement.

Agents should omit irrelevant optional sections rather than generating meaningless content solely to fill the template.

## Evolution

Create a new template only when the same artifact structure is repeatedly needed.

Do not create templates speculatively.

Real project usage should drive template evolution.

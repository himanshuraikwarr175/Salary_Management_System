# AI usage notes

Assessment expects intentional use of AI tools while keeping engineering judgment.
This file records how AI was used on this project.

## Tools

- **Cursor** (agentic coding assistant) for scaffolding, APIs, tests, UI, and docs
- Human review for product scope, commit history, and local run / demo decisions

## How AI was used (by phase)

| Phase | AI helped with | Human judgment |
|-------|----------------|----------------|
| Requirements | Draft one-page goal / in-out scope | Kept MVP small; left payroll, SSO out |
| Architecture | Folder layout, API sketch, data model | Chose FastAPI + React/Vite + SQLite local; Postgres optional later |
| Backend | Models, salary service, analytics, seed, FX | Tests first for money/FX math; no JWT after trying then removing |
| Frontend | Dashboard / employees / detail screens | Simple HR flows over complex UI |
| Artifacts | Requirements, architecture, AI usage, trade-offs, performance, deploy, demo checklist | Incremental commits controlled by author |

## Example instruction style (not verbatim chat logs)

Prompts were typically scoped like:

- “Write a one-page requirements doc: goal, in-scope, deliberate out-of-scope + why.”
- “Add salary update service that writes history; unit tests with in-memory SQLite.”
- “Build React dashboard calling `/analytics/summary` with optional FX base currency.”
- “Remove JWT auth and restore open APIs.”

## Correctness checks (non-negotiable)

AI output was not trusted blindly. Before considering a step done:

1. `pytest` for core salary / analytics / seed / FX conversion (mocked FX provider)
2. Manual API checks via `/docs` when needed
3. Seed idempotency (~10k employees, skip if already filled)
4. Product constraint: answer org pay questions with per-currency totals + optional live Frankfurter rollup

## What we deliberately did *not* ask AI to build

- Full payroll engine, tax, approvals
- Heavy RBAC / SSO
- In-app LLM chatbot (assessment is AI-assisted *development*, not an AI product feature)

## Takeaway

AI accelerated boilerplate and first drafts. Scope cuts, test design, FX-as-optional-rollup, and commit messaging stayed human-owned so the repo shows clear engineering judgment—not maximum complexity.

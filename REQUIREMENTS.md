# ACME Employee Salary Management — Requirements

**Persona:** HR Manager  
**Scale:** ~10,000 employees across multiple countries  
**Date:** 2026-03-18

## Goal

Replace Excel-based salary tracking with a web app so the HR Manager can:

1. **Manage** employee salary records (view, search, update).
2. **Answer** org-level pay questions (totals, averages, breakdowns by country/department).

## In scope

| Area | Features |
|------|----------|
| **Employees** | List, search by name/ID, filter by country & department; view employee detail |
| **Salary** | View current salary (amount + currency); update salary; keep a simple change history |
| **Insights** | Dashboard: headcount, total payroll (by currency), avg salary; breakdowns by country and department |
| **Data** | Seed ~10,000 realistic employees across multiple countries |
| **Quality** | Unit tests for core salary/analytics logic; incremental commits; deployable app |

## Out of scope (deliberate)

| Left out | Why |
|----------|-----|
| Full payroll (payslips, tax, deductions, benefits) | Different product; this assessment is salary *data* + insights, not a payroll engine |
| Approvals / multi-step workflows | Adds process complexity without proving core HR salary management |
| Multi-role auth / SSO / fine-grained RBAC | Single HR Manager persona; simple optional login is enough if needed |
| Currency FX conversion / single-currency rollup | Real FX is noisy; show totals **per currency** instead |
| Mobile app, notifications, Excel import/export v1 | Nice-to-haves; not required for a clear MVP |
| Real-time collaboration / audit for compliance | Overkill for demo scale; keep a lightweight salary-change history only |

## Success criteria

- HR can find an employee and update salary in a few clicks.
- HR can answer: “Who do we pay, how much, and how does pay look by country/department?”
- Seeded data supports ~10k employees without feeling broken (pagination / filters).
- Tests cover core calculation and update rules; app is deployed with a short demo video.

## Proposed stack (for next steps)

- **UI:** Next.js (React) + a component library (e.g. shadcn/ui or MUI)
- **Backend:** Next.js API routes (or separate Node API) + **SQLite** (simple, portable, enough for 10k rows)
- **Seed:** Script generating 10,000 employees
- **Tests:** Unit tests for salary update + analytics aggregations

## Non-goals for v1 UX

Not a “dashboard of everything.” Primary flows: **find employee → edit salary**, and **see org pay insights**. Cleanness over feature count.

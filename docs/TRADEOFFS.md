# Trade-offs

Decisions that shaped this MVP. Reviewers: complexity was cut on purpose.

## Product

| Choice | Alternative | Why we chose this |
|--------|-------------|-------------------|
| Salary data + insights | Full payroll (tax, payslips, runs) | Brief asks manage salaries + answer pay questions — not a payroll engine |
| Single HR persona, no auth | JWT / SSO / RBAC | One persona; auth adds ceremony without proving core domain |
| Optional live FX rollup | Force everything into one currency only, or no FX | Per-currency totals stay honest; Frankfurter rollup answers “org-wide” questions when network works |
| Soft salary history | Full compliance audit log | Enough to show change tracking for demo scale |
| No Excel import/export v1 | Bulk CSV tools | Nice-to-have; search/update/insights cover the Excel pain |

## Technical

| Choice | Alternative | Why |
|--------|-------------|-----|
| FastAPI + React/Vite | Next.js monolith | Clear API/UI split; easy pytest; matches common backend+SPA assessment shape |
| SQLite by default | Postgres-only | Zero friction locally + Docker volume; relational model still portable to Postgres via `DATABASE_URL` |
| Docker Compose (API + UI) | Compose with full Postgres always | Demo one-command; less moving parts for reviewers |
| Service layer for salary/FX | Logic only in route handlers | Fast, deterministic unit tests without HTTP |
| In-memory FX cache (1h) | Hit Frankfurter every request | Protects rate limits; analytics stay snappy |
| Stdlib-friendly deps where possible | Extra auth/JWT packages | Fewer install failures; keep MVP lean |

## Explicitly rejected (for now)

- Hire wizard / salary component catalogs / payment status workflows  
- Mobile app / notifications  
- In-app LLM chatbot (assessment is AI-assisted *build*, not an AI product feature)

If time remains after deploy + demo video, the highest-value add-ons would be Postgres in Compose and a simple login — not more payroll surface area.

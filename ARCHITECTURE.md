# Architecture — ACME Salary Management System

**Persona:** HR Manager  
**Scale:** ~10,000 employees   
**Related:** `REQUIREMENTS.md`

---

## 1. Goal of this design

HR can:

1. Find employees and update salaries.
2. Answer org pay questions (totals / averages / breakdowns).

We keep a **production-style** shape (separate backend/frontend, relational DB, Docker), with a deliberately small product surface.

---

## 2. High-level stack

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | **FastAPI** + SQLAlchemy | Fast APIs, OpenAPI `/docs`, easy pytest |
| DB | **SQLite** default (Postgres optional via `DATABASE_URL`) | Simple local/Docker demo; portable schema |
| Frontend | **React + TypeScript + Vite** | Clear SPA |
| Styling | **Tailwind CSS** | Fast, consistent UI |
| Data fetching | **TanStack Query** | Cache + loading/error states |
| FX | **Frankfurter** (`api.frankfurter.dev`) | Optional org-wide rollup; cached |
| Tests | **pytest** | Fast deterministic backend tests |
| Run | **Docker Compose** | UI `:8080` + API `:8000` |

**Ports:**

| Service | Docker | Local |
|---------|--------|--------|
| UI | http://localhost:8080 | http://localhost:5173 |
| API | http://localhost:8000 | http://localhost:8000 |
| API docs | http://localhost:8000/docs | same |
| Health | http://localhost:8000/health | same |

More diagrams: `docs/ARCHITECTURE_DIAGRAM.md`. Trade-offs: `docs/TRADEOFFS.md`. Performance: `docs/PERFORMANCE.md`.

---

## 3. Folder map —

Salary_Management_System/
├── REQUIREMENTS.md          # Product: goal, scope, out-of-scope
├── ARCHITECTURE.md          # This file: how we build it
├── README.md                # How to run / test (filled later)
├── docker-compose.yml       # postgres + backend + frontend
├── docs/                    # Trade-offs, AI usage notes, demo notes
│
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, routers
│   │   ├── config.py        # Settings (DB URL, CORS)
│   │   ├── db.py            # Engine, session
│   │   ├── models/          # SQLAlchemy tables
│   │   ├── schemas/         # Pydantic request/response
│   │   ├── api/             # Route handlers (/api/v1/...)
│   │   ├── services/        # Business logic (salary, analytics)
│   │   └── seed/            # Seed ~10k employees
│   ├── tests/               # pytest
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── pages/           # Dashboard, Employees list, Employee detail
    │   ├── components/      # Table, filters, salary form, charts
    │   ├── api/             # fetch helpers to backend
    │   ├── hooks/           # TanStack Query hooks
    │   └── types/           # Shared TS types
    ├── package.json
    └── vite.config.ts       # Proxy /api → :8000 in local dev
```

|       Piece |       Responsibility |             Why separate        |
|-------------|----------------------|---------------------------------|
|    `api/`   |       HTTP only      | Thin controllers                |
| `services/` | Rules + aggregations | Easy to unit test               |
| `models/`   | DB shape             |  One source of truth for tables |
| `schemas/`  | API contract         | Validation + docs               |
| `pages/`    | Screens HR uses      | Clear UX map                    |
| `seed/`     | Demo data            | Reproducible 10k dataset        |

---

## 4. Data model (MVP)

Keep master data **simple** (columns / enums), not a full admin CRUD app on day one.

### `employees`

| Column                  | Notes                          |
|-------------------------|--------------------------------|
| id                      | UUID or serial PK              |
| employee_code           | Human-readable ID (searchable) |
| full_name               |                                |
| email                   | Unique                         |
| country_code            | e.g. IN, US, DE                |
| department              | e.g. Engineering, HR, Sales    |
| job_title               |                                |
| currency_code           | e.g. INR, USD, EUR             |
| annual_salary           | Numeric (current package)      |
| hire_date               |                                |
| is_active               | Soft filter                    |
| created_at / updated_at |                                |

### `salary_history`

| Column               |        Notes   |
|----------------------|----------------|
| id                   | PK             |
| employee_id          | FK → employees |
|old_salary/new_salary |                |
| currency_code        |                |
| changed_at           |                |
| note                 | Optional reason|

**Indexes (performance for 10k):**

- `employees(full_name)`, `employees(employee_code)`
- `employees(country_code)`, `employees(department)`
- `salary_history(employee_id, changed_at DESC)`


---

## 5. API sketch (`/api/v1`)

| Method |                  Path                 |                 Purpose             |
|--------|-------------------------- ------------|-------------------------------------|
| GET    | `/health`                             | Liveness (no prefix or top-level)   |
| GET    | `/api/v1/employees`                   | List + search + filters + pagination|
| GET    | `/api/v1/employees/{id}`              | Detail                              |
| PATCH  | `/api/v1/employees/{id}/salary`       | Update salary + write history       |
| GET    |`/api/v1/employees/{id}/salary-history`|   Recent changes                    |
| GET    | `/api/v1/analytics/summary`           | Headcount, totals **per currency**, averages |
| GET    | `/api/v1/analytics/by-country`        | Breakdown                           |
| GET    | `/api/v1/analytics/by-department`     | Breakdown                           |

**List query params (example):**  
`q`, `country`, `department`, `page`, `page_size`, `sort`

**Salary update rule (service layer):**

1. Validate amount > 0.
2. Read current salary.
3. Update `employees.annual_salary`.
4. Insert `salary_history` row.
5. Return updated employee.

Interactive docs: `http://localhost:8000/docs`

---

## 6. UI screens (MVP)

| Scree          |  Route (SPA)    |        What HR does                                     |
|----------------|-----------------|---------------------------------------------------------|
| Dashboard      | `/`             | See headcount, pay by currency, country/dept breakdowns |
| Employees      | `/employees`    | Search, filter, paginate                                |
| Employee detail| `/employees/:id`| View profile, edit salary, see history                  |

**Local workflow:** Vite on 5173 proxies `/api` → backend 8000.  
**Docker workflow:** Nginx serves built UI on 8080 and proxies API.

---

## 7. End-to-end workflow (kaise data chalti hai)

```text
Browser (React)
    │  TanStack Query → GET/PATCH /api/v1/...
    ▼
FastAPI routers (api/)
    │
    ▼
services/  (validate, update salary, aggregate analytics)
    │
    ▼
SQLAlchemy → PostgreSQL
    ▲
seed/ (first boot or `python -m app.seed.seed_data`)
```

**Primary HR flows:**

1. **Find → edit salary:** Employees → open row → PATCH salary → history updates → list/detail refresh.  
2. **Org questions:** Dashboard loads analytics endpoints → charts/tables (totals **per currency**, no forced single FX rollup in v1).

---

## 8. Seeding (~10,000 employees)

- Faker (or similar) for names; fixed pools for countries, departments, currencies, salary bands.
- Idempotent strategy: seed only if `employees` count is 0 (Docker-friendly).
- First Docker boot may take a few minutes — expected.

---

## 9. How to test (so you understand each layer)

| Layer | How | What it proves |
|-------|-----|----------------|
| Unit / service | `cd backend && pytest -v` | Salary update + analytics math correct |
| API | Swagger `/docs` or curl | Routes + validation work |
| Seed | Count rows in DB / logs | ~10k loaded |
| UI | `npm run dev` or Docker `:8080` | HR can search + edit + see dashboard |
| Manual checklist | Search name, filter country, change salary, refresh analytics | Product goal met |

**Debug order when something breaks:** UI → Network tab → API response → service logic → DB row.

---

## 10. Trade-offs (vs friend’s fuller app)

| Friend’s README | Our choice | Why |
|-----------------|------------|-----|
| Hire wizard, salary components, payment status | Out of v1 | Scope creep; not needed to prove salary *management* + insights |
| Live FX / exchange-rates | **In** (optional rollup) | Per-currency native totals remain; Frankfurter for org-wide view |
| Master-data admin CRUD | Seeded constants / columns | Enough for filters + analytics |
| Same ports, FastAPI, React Vite, Docker | **In** | Familiar, reviewable |
| Postgres always-on | SQLite default | Faster demo path; Postgres still supported via env |
---

## 11. Performance notes (10k)

- Server-side **pagination** (never send all 10k to the browser).
- Indexes on filter/search columns.
- Analytics via SQL `GROUP BY`, not Python loops over all rows.
- Connection pooling (SQLAlchemy defaults / tuned in config).

---

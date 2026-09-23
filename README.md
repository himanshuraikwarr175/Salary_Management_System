# ACME Salary Management

Web app for HR to manage and analyze compensation for ~10,000 employees.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI + SQLAlchemy + SQLite (Postgres optional) |
| Frontend | React + TypeScript + Vite + Tailwind + TanStack Query |
| Tests | pytest |
| FX | Frankfurter (optional payroll rollup) |
| Run | Docker Compose or local dev servers |

## Artifacts (assessment)

| Doc | Purpose |
|-----|---------|
| `REQUIREMENTS.md` | Goal, scope, out-of-scope |
| `ARCHITECTURE.md` | Design + folder/API map |
| `docs/ARCHITECTURE_DIAGRAM.md` | Mermaid diagrams |
| `docs/AI_USAGE.md` | How AI tools were used |
| `docs/TRADEOFFS.md` | Product/tech trade-offs |
| `docs/PERFORMANCE.md` | 10k-scale considerations |
| `docs/DEPLOY.md` | Deploy options |
| `docs/DEMO_CHECKLIST.md` | Video script |
| `docs/SUBMISSION.md` | Email + links checklist |

## 1. Run with Docker (recommended for demo)

```bash
docker compose up -d --build
```

| Service | URL |
|---------|-----|
| App UI | **http://localhost:8080** |
| API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

First boot seeds ~10k employees (may take a few minutes).

```bash
docker compose logs -f backend
docker compose down          # keep DB volume
docker compose down -v       # wipe + re-seed next time
```

## 2. Run locally (hot reload)

### Backend (port 8000)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # optional
python -m app.seed.seed_data
uvicorn app.main:app --reload --port 8000
```

### Frontend (port 5173)

```bash
cd frontend
npm install
cp .env.example .env          # optional; leave VITE_API_BASE_URL empty for proxy
npm run dev
```

Open http://localhost:5173

Or use `make test` / `make up` from the repo root.

## What you can do

- **Dashboard** — headcount; per-currency totals; live FX rollup; country/dept breakdowns  
- **Employees** — search, filter, paginate  
- **Employee detail** — update salary + history  

## Tests

```bash
cd backend && source .venv/bin/activate && pytest -v
```

## Deploy & submit

See `docs/DEPLOY.md` and `docs/SUBMISSION.md`.

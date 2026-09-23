# ACME Salary Management

Web app for HR to manage and analyze compensation for ~10,000 employees.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI + SQLAlchemy + SQLite (local / Docker volume) |
| Frontend | React + TypeScript + Vite + Tailwind + TanStack Query |
| Tests | pytest |
| FX | Frankfurter (optional payroll rollup) |

## Docs / artifacts

- `REQUIREMENTS.md` — product scope
- `ARCHITECTURE.md` — design notes
- `docs/AI_USAGE.md` — how AI tools were used

## 1. Run with Docker (recommended for demo)

**Prerequisites:** Docker + Docker Compose.

```bash
docker compose up -d --build
```

| Service | URL |
|---------|-----|
| App UI | **http://localhost:8080** |
| API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |

First boot seeds ~10k employees into a SQLite volume (can take a few minutes). Later starts skip seeding if data exists.

```bash
docker compose logs -f backend   # seed progress
docker compose ps
docker compose down              # keep volume
docker compose down -v           # wipe DB + re-seed next up
```

## 2. Run locally (hot reload)

### Backend (port 8000)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed.seed_data
uvicorn app.main:app --reload --port 8000
```

### Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — Vite proxies `/api` to the backend.

## What you can do

- **Dashboard** — headcount; totals/averages per currency; live FX rollup; country & department breakdowns
- **Employees** — search, filter, paginate
- **Employee detail** — update salary + history

## Tests

```bash
cd backend
source .venv/bin/activate
pytest -v
```

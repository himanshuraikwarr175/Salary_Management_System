# ACME Salary Management

Web app for HR to manage and analyze compensation for ~10,000 employees.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI + SQLAlchemy + SQLite (local) |
| Frontend | React + TypeScript + Vite + Tailwind + TanStack Query |
| Tests | pytest |

## Run locally

### Backend (port 8000)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed.seed_data          # first time — seeds ~10k employees
uvicorn app.main:app --reload --port 8000
```

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

Vite proxies `/api` and `/health` to the backend.

## What you can do

- **Dashboard** — headcount and pay totals/averages per currency; country & department breakdowns
- **Employees** — search, filter, paginate
- **Employee detail** — view profile, update salary, see change history

## Tests

```bash
cd backend
source .venv/bin/activate
pytest -v
```

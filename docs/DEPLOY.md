# Deploy guide

Assessment asks for a **fully functional deployed** app. This repo is ready for:

1. **Docker host** (easiest if you already use Compose), or  
2. **Split host** — API on Render/Railway, UI on Vercel/Netlify.

Replace placeholders with your real URLs after deploy. Put the live link in the submission email with the GitHub repo.

## A. Docker on a VPS / Railway / Fly (single stack)

Repo already has `docker-compose.yml`:

- UI: port **8080** (nginx proxies `/api` → backend)  
- API: port **8000**  
- SQLite on volume `salary_data`  
- First boot seeds ~10k employees  

```bash
docker compose up -d --build
```

Point a domain / public IP at `:8080`. Ensure outbound HTTPS works so Frankfurter FX can load.

## B. Split deploy (common free-tier path)

### Backend (Render Web Service example)

1. New **Web Service** from this GitHub repo  
2. Root directory: `backend`  
3. Runtime: Docker **or** native:

| Setting | Value |
|---------|--------|
| Build | `pip install -r requirements.txt` |
| Start | `python -m app.seed.seed_data && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Env vars:

```text
DATABASE_URL=sqlite:///./data/salary.db
CORS_ORIGINS=https://YOUR-FRONTEND.vercel.app
FX_API_BASE=https://api.frankfurter.dev/v1
```

Use a persistent disk for SQLite on Render, **or** set `DATABASE_URL` to a free Postgres URL (SQLAlchemy URL form).

Health check path: `/health`

### Frontend (Vercel / Netlify)

1. Root: `frontend`  
2. Build: `npm install && npm run build`  
3. Output: `dist`  
4. Env at **build** time:

```text
VITE_API_BASE_URL=https://YOUR-API.onrender.com
```

(No trailing slash.) The SPA will call `${VITE_API_BASE_URL}/api/v1/...`.

## C. After deploy — smoke test

- [ ] `/health` → `{"status":"ok"}`  
- [ ] UI loads dashboard  
- [ ] Employees search returns rows  
- [ ] Salary update writes history  
- [ ] FX rollup works (or shows graceful error if blocked)

## D. Submission bundle

1. GitHub repo link (incremental commits visible)  
2. Live app URL  
3. Short demo video (see `docs/DEMO_CHECKLIST.md`)  
4. Reply on the same assessment email  

Fill live URLs into `docs/SUBMISSION.md` when ready.

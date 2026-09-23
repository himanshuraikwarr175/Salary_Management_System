.PHONY: test seed api ui up down

test:
	cd backend && .venv/bin/pytest -v

seed:
	cd backend && .venv/bin/python -m app.seed.seed_data

api:
	cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000

ui:
	cd frontend && npm run dev

up:
	docker compose up -d --build

down:
	docker compose down

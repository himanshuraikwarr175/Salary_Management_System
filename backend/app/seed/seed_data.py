"""Generate and load demo employees (~10,000 by default)."""

from __future__ import annotations

import random
from datetime import date, timedelta
from decimal import Decimal

from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal, init_db
from app.models import Employee

COUNTRY_CURRENCY = {
    "US": ("USD", (55_000, 180_000)),
    "IN": ("INR", (400_000, 4_500_000)),
    "GB": ("GBP", (35_000, 120_000)),
    "DE": ("EUR", (40_000, 130_000)),
    "CA": ("CAD", (50_000, 150_000)),
    "AU": ("AUD", (55_000, 160_000)),
    "SG": ("SGD", (45_000, 140_000)),
    "JP": ("JPY", (3_500_000, 12_000_000)),
}

DEPARTMENTS = [
    "Engineering",
    "Sales",
    "HR",
    "Finance",
    "Marketing",
    "Operations",
    "Product",
    "Customer Success",
]

JOB_TITLES = {
    "Engineering": ["Software Engineer", "Senior Engineer", "Staff Engineer", "QA Engineer"],
    "Sales": ["Account Executive", "Sales Manager", "SDR"],
    "HR": ["HR Generalist", "HR Manager", "Recruiter"],
    "Finance": ["Accountant", "Financial Analyst", "Controller"],
    "Marketing": ["Marketing Specialist", "Content Lead", "Growth Manager"],
    "Operations": ["Operations Analyst", "Ops Manager"],
    "Product": ["Product Manager", "Product Designer", "Researcher"],
    "Customer Success": ["CSM", "Support Specialist", "Support Lead"],
}


def _salary_for(country: str, rng: random.Random) -> tuple[str, Decimal]:
    currency, (low, high) = COUNTRY_CURRENCY[country]
    amount = Decimal(rng.randint(low, high)).quantize(Decimal("0.01"))
    return currency, amount


def build_employee(index: int, fake: Faker, rng: random.Random) -> Employee:
    country = rng.choice(list(COUNTRY_CURRENCY.keys()))
    department = rng.choice(DEPARTMENTS)
    currency, salary = _salary_for(country, rng)
    hire_days_ago = rng.randint(30, 3650)
    return Employee(
        employee_code=f"E{index:05d}",
        full_name=fake.name(),
        email=f"e{index:05d}@acme.test",
        country_code=country,
        department=department,
        job_title=rng.choice(JOB_TITLES[department]),
        currency_code=currency,
        annual_salary=salary,
        hire_date=date.today() - timedelta(days=hire_days_ago),
        is_active=rng.random() > 0.03,
    )


def seed_employees(
    db: Session,
    *,
    count: int | None = None,
    batch_size: int = 500,
    seed: int = 42,
) -> int:
    """
    Insert employees if the table is empty.
    Returns number of rows inserted (0 if already seeded).
    """
    target = count if count is not None else settings.seed_employee_count
    existing = db.scalar(select(func.count()).select_from(Employee)) or 0
    if existing > 0:
        print(f"Skip seed: employees already has {existing} rows")
        return 0

    fake = Faker()
    Faker.seed(seed)
    rng = random.Random(seed)

    inserted = 0
    batch: list[Employee] = []
    for i in range(1, target + 1):
        batch.append(build_employee(i, fake, rng))
        if len(batch) >= batch_size:
            db.add_all(batch)
            db.commit()
            inserted += len(batch)
            print(f"Seeded {inserted}/{target}")
            batch = []

    if batch:
        db.add_all(batch)
        db.commit()
        inserted += len(batch)
        print(f"Seeded {inserted}/{target}")

    return inserted


def main() -> None:
    print(f"DB: {settings.database_url}")
    init_db()
    db = SessionLocal()
    try:
        inserted = seed_employees(db)
        total = db.scalar(select(func.count()).select_from(Employee)) or 0
        print(f"Done. inserted={inserted}, total_employees={total}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

"""In-memory SQLite checks that models map without needing Postgres."""

from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import Employee, SalaryHistory


def test_employee_and_salary_history_tables():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        emp = Employee(
            employee_code="E0001",
            full_name="Ada Lovelace",
            email="ada@acme.test",
            country_code="GB",
            department="Engineering",
            job_title="Engineer",
            currency_code="GBP",
            annual_salary=Decimal("90000.00"),
            hire_date=date(2020, 1, 15),
            is_active=True,
        )
        db.add(emp)
        db.flush()

        history = SalaryHistory(
            employee_id=emp.id,
            old_salary=Decimal("85000.00"),
            new_salary=Decimal("90000.00"),
            currency_code="GBP",
            note="Annual review",
        )
        db.add(history)
        db.commit()

        saved = db.get(Employee, emp.id)
        assert saved is not None
        assert saved.employee_code == "E0001"
        assert len(saved.salary_history) == 1
        assert saved.salary_history[0].new_salary == Decimal("90000.00")
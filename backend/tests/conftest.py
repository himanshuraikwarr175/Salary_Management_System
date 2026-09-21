"""Shared in-memory SQLite session for service/unit tests."""

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base
from app.models import Employee


@pytest.fixture()
def db() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def employee(db: Session) -> Employee:
    emp = Employee(
        employee_code="E1001",
        full_name="Grace Hopper",
        email="grace@acme.test",
        country_code="US",
        department="Engineering",
        job_title="Engineer",
        currency_code="USD",
        annual_salary=Decimal("100000.00"),
        hire_date=date(2018, 6, 1),
        is_active=True,
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

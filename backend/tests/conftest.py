"""Shared fixtures for service and API tests (in-memory SQLite)."""

from collections.abc import Generator
from datetime import date
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Employee


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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


@pytest.fixture()
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

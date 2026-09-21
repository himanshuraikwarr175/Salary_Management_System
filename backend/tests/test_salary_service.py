from decimal import Decimal

import pytest

from app.models import Employee, SalaryHistory
from app.services.salary import (
    EmployeeNotFoundError,
    InvalidSalaryError,
    list_salary_history,
    update_employee_salary,
)


def test_update_salary_writes_history(db, employee):
    updated = update_employee_salary(
        db,
        employee.id,
        "110000.50",
        note="Promotion",
    )

    assert updated.annual_salary == Decimal("110000.50")

    history = db.query(SalaryHistory).filter_by(employee_id=employee.id).all()
    assert len(history) == 1
    assert history[0].old_salary == Decimal("100000.00")
    assert history[0].new_salary == Decimal("110000.50")
    assert history[0].currency_code == "USD"
    assert history[0].note == "Promotion"


def test_update_salary_rejects_zero_and_negative(db, employee):
    with pytest.raises(InvalidSalaryError):
        update_employee_salary(db, employee.id, 0)

    with pytest.raises(InvalidSalaryError):
        update_employee_salary(db, employee.id, -1)

    # Employee salary unchanged
    saved = db.get(Employee, employee.id)
    assert saved is not None
    assert saved.annual_salary == Decimal("100000.00")


def test_update_salary_rejects_missing_employee(db):
    with pytest.raises(EmployeeNotFoundError):
        update_employee_salary(db, 99999, 50000)


def test_list_salary_history_newest_first(db, employee):
    update_employee_salary(db, employee.id, 105000, note="First")
    update_employee_salary(db, employee.id, 120000, note="Second")

    rows = list_salary_history(db, employee.id)
    assert len(rows) == 2
    assert rows[0].new_salary == Decimal("120000.00")
    assert rows[1].new_salary == Decimal("105000.00")

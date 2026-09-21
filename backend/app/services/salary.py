"""Business logic for salary updates."""

from decimal import Decimal, InvalidOperation
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Employee, SalaryHistory


class EmployeeNotFoundError(Exception):
    def __init__(self, employee_id: int) -> None:
        self.employee_id = employee_id
        super().__init__(f"Employee {employee_id} not found")


class InvalidSalaryError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def _to_money(value: Decimal | int | float | str) -> Decimal:
    try:
        amount = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise InvalidSalaryError("Salary must be a valid number") from exc

    if amount <= 0:
        raise InvalidSalaryError("Salary must be greater than zero")

    # Money stored with 2 decimal places
    return amount.quantize(Decimal("0.01"))


def update_employee_salary(
    db: Session,
    employee_id: int,
    new_salary: Decimal | int | float | str,
    note: Optional[str] = None,
) -> Employee:
    """
    Update an employee's annual salary and append a salary_history row.

    Raises:
        EmployeeNotFoundError: if employee_id does not exist
        InvalidSalaryError: if new_salary is invalid
    """
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise EmployeeNotFoundError(employee_id)

    amount = _to_money(new_salary)
    old_salary = Decimal(employee.annual_salary).quantize(Decimal("0.01"))

    history = SalaryHistory(
        employee_id=employee.id,
        old_salary=old_salary,
        new_salary=amount,
        currency_code=employee.currency_code,
        note=note,
    )
    employee.annual_salary = amount
    db.add(history)
    db.commit()
    db.refresh(employee)
    return employee


def list_salary_history(
    db: Session,
    employee_id: int,
    *,
    limit: int = 50,
) -> list[SalaryHistory]:
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise EmployeeNotFoundError(employee_id)

    return (
        db.query(SalaryHistory)
        .filter(SalaryHistory.employee_id == employee_id)
        .order_by(SalaryHistory.changed_at.desc())
        .limit(limit)
        .all()
    )
"""Employee query helpers."""

from typing import Optional

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models import Employee
from app.services.salary import EmployeeNotFoundError


def get_employee(db: Session, employee_id: int) -> Employee:
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise EmployeeNotFoundError(employee_id)
    return employee


def list_employees(
    db: Session,
    *,
    q: Optional[str] = None,
    country: Optional[str] = None,
    department: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Employee], int]:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)

    filters = []
    if q:
        pattern = f"%{q.strip()}%"
        filters.append(
            or_(
                Employee.full_name.ilike(pattern),
                Employee.employee_code.ilike(pattern),
                Employee.email.ilike(pattern),
            )
        )
    if country:
        filters.append(Employee.country_code == country.upper())
    if department:
        filters.append(Employee.department == department)

    base: Select = select(Employee)
    count_stmt: Select = select(func.count()).select_from(Employee)
    if filters:
        for f in filters:
            base = base.where(f)
            count_stmt = count_stmt.where(f)

    total = db.scalar(count_stmt) or 0
    items = (
        db.scalars(
            base.order_by(Employee.full_name.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        .all()
    )
    return list(items), int(total)
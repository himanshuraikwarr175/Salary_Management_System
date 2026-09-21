"""Org-level compensation analytics (per currency — no FX conversion)."""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Employee


def summary_analytics(db: Session) -> dict:
    headcount = db.scalar(
        select(func.count()).select_from(Employee).where(Employee.is_active.is_(True))
    ) or 0

    rows = db.execute(
        select(
            Employee.currency_code,
            func.count(Employee.id),
            func.sum(Employee.annual_salary),
            func.avg(Employee.annual_salary),
        )
        .where(Employee.is_active.is_(True))
        .group_by(Employee.currency_code)
        .order_by(Employee.currency_code.asc())
    ).all()

    by_currency = [
        {
            "currency_code": currency,
            "headcount": int(count),
            "total_annual_salary": Decimal(str(total or 0)).quantize(Decimal("0.01")),
            "avg_annual_salary": Decimal(str(avg or 0)).quantize(Decimal("0.01")),
        }
        for currency, count, total, avg in rows
    ]

    return {"headcount": int(headcount), "by_currency": by_currency}


def breakdown_by_country(db: Session) -> list[dict]:
    rows = db.execute(
        select(
            Employee.country_code,
            Employee.currency_code,
            func.count(Employee.id),
            func.sum(Employee.annual_salary),
            func.avg(Employee.annual_salary),
        )
        .where(Employee.is_active.is_(True))
        .group_by(Employee.country_code, Employee.currency_code)
        .order_by(Employee.country_code.asc(), Employee.currency_code.asc())
    ).all()

    return [
        {
            "country_code": country,
            "currency_code": currency,
            "headcount": int(count),
            "total_annual_salary": Decimal(str(total or 0)).quantize(Decimal("0.01")),
            "avg_annual_salary": Decimal(str(avg or 0)).quantize(Decimal("0.01")),
        }
        for country, currency, count, total, avg in rows
    ]


def breakdown_by_department(db: Session) -> list[dict]:
    rows = db.execute(
        select(
            Employee.department,
            Employee.currency_code,
            func.count(Employee.id),
            func.sum(Employee.annual_salary),
            func.avg(Employee.annual_salary),
        )
        .where(Employee.is_active.is_(True))
        .group_by(Employee.department, Employee.currency_code)
        .order_by(Employee.department.asc(), Employee.currency_code.asc())
    ).all()

    return [
        {
            "department": department,
            "currency_code": currency,
            "headcount": int(count),
            "total_annual_salary": Decimal(str(total or 0)).quantize(Decimal("0.01")),
            "avg_annual_salary": Decimal(str(avg or 0)).quantize(Decimal("0.01")),
        }
        for department, currency, count, total, avg in rows
    ]

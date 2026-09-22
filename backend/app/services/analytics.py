"""Org-level compensation analytics (per currency + optional FX rollup)."""

from decimal import Decimal
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Employee
from app.services.fx import FxError, convert_amount, get_rates_vs_base


def summary_analytics(
    db: Session,
    *,
    base_currency: Optional[str] = None,
) -> dict:
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

    target = (base_currency or settings.fx_default_base or "USD").upper()
    result: dict = {
        "headcount": int(headcount),
        "by_currency": by_currency,
        "base_currency": target,
        "total_in_base": None,
        "avg_in_base": None,
        "fx_as_of": None,
        "fx_source": None,
        "fx_error": None,
    }

    if headcount == 0:
        return result

    try:
        # Frankfurter rates with from=USD → units of C per 1 USD
        as_of, rates_vs_usd = get_rates_vs_base("USD")
        rates_vs_usd = {**rates_vs_usd, "USD": Decimal("1")}

        total_base = Decimal("0.00")
        for row in by_currency:
            total_base += convert_amount(
                row["total_annual_salary"],
                row["currency_code"],
                target,
                rates_vs_usd,
            )

        result.update(
            {
                "total_in_base": total_base,
                "avg_in_base": (total_base / Decimal(headcount)).quantize(
                    Decimal("0.01")
                ),
                "fx_as_of": as_of,
                "fx_source": "frankfurter",
            }
        )
    except FxError as exc:
        result["fx_error"] = str(exc)

    return result


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

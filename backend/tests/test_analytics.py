from datetime import date
from decimal import Decimal

from app.models import Employee
from app.services.analytics import (
    breakdown_by_country,
    breakdown_by_department,
    summary_analytics,
)
from app.services.fx import clear_fx_cache, convert_amount, get_rates_vs_base


def _add_employee(db, **kwargs) -> Employee:
    defaults = {
        "job_title": "Staff",
        "hire_date": date(2020, 1, 1),
        "is_active": True,
    }
    defaults.update(kwargs)
    emp = Employee(**defaults)
    db.add(emp)
    db.commit()
    return emp


def test_summary_per_currency(db):
    clear_fx_cache()

    def fake_fetch(_base: str):
        return "2026-03-18", {
            "USD": Decimal("1"),
            "INR": Decimal("80"),
            "EUR": Decimal("0.9"),
        }

    # Patch via injecting fetch into cache by calling get_rates with fetch
    get_rates_vs_base("USD", fetch=fake_fetch)

    _add_employee(
        db,
        employee_code="A1",
        full_name="One",
        email="one@acme.test",
        country_code="US",
        department="Engineering",
        currency_code="USD",
        annual_salary=Decimal("100000"),
    )
    _add_employee(
        db,
        employee_code="A2",
        full_name="Two",
        email="two@acme.test",
        country_code="IN",
        department="Engineering",
        currency_code="INR",
        annual_salary=Decimal("2000000"),
    )
    _add_employee(
        db,
        employee_code="A3",
        full_name="Three",
        email="three@acme.test",
        country_code="US",
        department="Sales",
        currency_code="USD",
        annual_salary=Decimal("80000"),
    )

    result = summary_analytics(db, base_currency="USD")
    assert result["headcount"] == 3
    by_ccy = {row["currency_code"]: row for row in result["by_currency"]}
    assert by_ccy["USD"]["headcount"] == 2
    assert by_ccy["USD"]["total_annual_salary"] == Decimal("180000.00")
    assert by_ccy["INR"]["headcount"] == 1
    # 180000 USD + 2000000/80 INR = 180000 + 25000 = 205000
    assert result["total_in_base"] == Decimal("205000.00")
    assert result["fx_source"] == "frankfurter"
    assert result["fx_error"] is None


def test_convert_amount_helpers():
    rates = {"USD": Decimal("1"), "INR": Decimal("80"), "EUR": Decimal("0.9")}
    assert convert_amount(Decimal("8000"), "INR", "USD", rates) == Decimal("100.00")
    assert convert_amount(Decimal("90"), "EUR", "USD", rates) == Decimal("100.00")
    assert convert_amount(Decimal("100"), "USD", "INR", rates) == Decimal("8000.00")


def test_breakdown_by_country_and_department(db):
    _add_employee(
        db,
        employee_code="B1",
        full_name="US Eng",
        email="useng@acme.test",
        country_code="US",
        department="Engineering",
        currency_code="USD",
        annual_salary=Decimal("120000"),
    )
    _add_employee(
        db,
        employee_code="B2",
        full_name="IN Sales",
        email="insales@acme.test",
        country_code="IN",
        department="Sales",
        currency_code="INR",
        annual_salary=Decimal("1500000"),
    )

    countries = breakdown_by_country(db)
    assert len(countries) == 2
    assert countries[0]["country_code"] == "IN"

    departments = breakdown_by_department(db)
    assert {d["department"] for d in departments} == {"Engineering", "Sales"}


def test_analytics_api_endpoints(client, db, monkeypatch):
    clear_fx_cache()

    def fake_fetch(_base: str):
        return "2026-03-18", {
            "USD": Decimal("1"),
            "EUR": Decimal("0.9"),
            "INR": Decimal("80"),
        }

    monkeypatch.setattr(
        "app.services.fx._default_fetch",
        fake_fetch,
    )

    _add_employee(
        db,
        employee_code="C1",
        full_name="API User",
        email="api@acme.test",
        country_code="DE",
        department="HR",
        currency_code="EUR",
        annual_salary=Decimal("70000"),
    )

    summary = client.get("/api/v1/analytics/summary", params={"base_currency": "USD"})
    assert summary.status_code == 200
    body = summary.json()
    assert body["headcount"] == 1
    # 70000 EUR / 0.9 = 77777.78 USD
    assert body["total_in_base"] == "77777.78"
    assert body["fx_error"] is None

    by_country = client.get("/api/v1/analytics/by-country")
    assert by_country.status_code == 200
    assert by_country.json()[0]["country_code"] == "DE"

    by_dept = client.get("/api/v1/analytics/by-department")
    assert by_dept.status_code == 200
    assert by_dept.json()[0]["department"] == "HR"

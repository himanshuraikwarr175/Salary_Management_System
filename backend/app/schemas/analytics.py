from decimal import Decimal

from pydantic import BaseModel


class CurrencyAggregate(BaseModel):
    currency_code: str
    headcount: int
    total_annual_salary: Decimal
    avg_annual_salary: Decimal


class AnalyticsSummaryOut(BaseModel):
    headcount: int
    by_currency: list[CurrencyAggregate]


class CountryBreakdownOut(BaseModel):
    country_code: str
    currency_code: str
    headcount: int
    total_annual_salary: Decimal
    avg_annual_salary: Decimal


class DepartmentBreakdownOut(BaseModel):
    department: str
    currency_code: str
    headcount: int
    total_annual_salary: Decimal
    avg_annual_salary: Decimal

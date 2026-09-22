from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class CurrencyAggregate(BaseModel):
    currency_code: str
    headcount: int
    total_annual_salary: Decimal
    avg_annual_salary: Decimal


class AnalyticsSummaryOut(BaseModel):
    headcount: int
    by_currency: list[CurrencyAggregate]
    base_currency: Optional[str] = None
    total_in_base: Optional[Decimal] = None
    avg_in_base: Optional[Decimal] = None
    fx_as_of: Optional[str] = None
    fx_source: Optional[str] = None
    fx_error: Optional[str] = None


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

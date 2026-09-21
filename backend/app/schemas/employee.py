from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_code: str
    full_name: str
    email: str
    country_code: str
    department: str
    job_title: str
    currency_code: str
    annual_salary: Decimal
    hire_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime


class EmployeeListOut(BaseModel):
    items: list[EmployeeOut]
    total: int
    page: int
    page_size: int


class SalaryUpdateIn(BaseModel):
    annual_salary: Decimal = Field(..., gt=0, decimal_places=2)
    note: Optional[str] = None


class SalaryHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    old_salary: Decimal
    new_salary: Decimal
    currency_code: str
    changed_at: datetime
    note: Optional[str] = None

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.salary_history import SalaryHistory


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        Index("ix_employees_full_name", "full_name"),
        Index("ix_employees_employee_code", "employee_code"),
        Index("ix_employees_country_code", "country_code"),
        Index("ix_employees_department", "department"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    job_title: Mapped[str] = mapped_column(String(150), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    annual_salary: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    salary_history: Mapped[list["SalaryHistory"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan",
        order_by="SalaryHistory.changed_at.desc()",
    )

    def __repr__(self) -> str:
        return f"<Employee {self.employee_code} {self.full_name}>"
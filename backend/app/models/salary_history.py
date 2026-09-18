from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.employee import Employee


class SalaryHistory(Base):
    __tablename__ = "salary_history"
    __table_args__ = (
        Index("ix_salary_history_employee_changed", "employee_id", "changed_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), nullable=False
    )
    old_salary: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    new_salary: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    employee: Mapped["Employee"] = relationship(back_populates="salary_history")

    def __repr__(self) -> str:
        return (
            f"<SalaryHistory emp={self.employee_id} "
            f"{self.old_salary}->{self.new_salary}>"
        )
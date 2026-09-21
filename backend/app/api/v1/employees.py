from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.employee import (
    EmployeeListOut,
    EmployeeOut,
    SalaryHistoryOut,
    SalaryUpdateIn,
)
from app.services.employees import get_employee, list_employees
from app.services.salary import (
    EmployeeNotFoundError,
    InvalidSalaryError,
    list_salary_history,
    update_employee_salary,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=EmployeeListOut)
def get_employees(
    q: Optional[str] = Query(None, description="Search name, code, or email"),
    country: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> EmployeeListOut:
    items, total = list_employees(
        db,
        q=q,
        country=country,
        department=department,
        page=page,
        page_size=page_size,
    )
    return EmployeeListOut(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee_detail(
    employee_id: int,
    db: Session = Depends(get_db),
) -> EmployeeOut:
    try:
        return get_employee(db, employee_id)
    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch("/{employee_id}/salary", response_model=EmployeeOut)
def patch_employee_salary(
    employee_id: int,
    body: SalaryUpdateIn,
    db: Session = Depends(get_db),
) -> EmployeeOut:
    try:
        return update_employee_salary(
            db,
            employee_id,
            body.annual_salary,
            note=body.note,
        )
    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidSalaryError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        ) from exc


@router.get("/{employee_id}/salary-history", response_model=list[SalaryHistoryOut])
def get_employee_salary_history(
    employee_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[SalaryHistoryOut]:
    try:
        return list_salary_history(db, employee_id, limit=limit)
    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

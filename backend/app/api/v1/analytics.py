from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.analytics import (
    AnalyticsSummaryOut,
    CountryBreakdownOut,
    DepartmentBreakdownOut,
)
from app.services import analytics as analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummaryOut)
def get_summary(db: Session = Depends(get_db)) -> AnalyticsSummaryOut:
    return AnalyticsSummaryOut(**analytics_service.summary_analytics(db))


@router.get("/by-country", response_model=list[CountryBreakdownOut])
def get_by_country(db: Session = Depends(get_db)) -> list[CountryBreakdownOut]:
    return [
        CountryBreakdownOut(**row)
        for row in analytics_service.breakdown_by_country(db)
    ]


@router.get("/by-department", response_model=list[DepartmentBreakdownOut])
def get_by_department(db: Session = Depends(get_db)) -> list[DepartmentBreakdownOut]:
    return [
        DepartmentBreakdownOut(**row)
        for row in analytics_service.breakdown_by_department(db)
    ]

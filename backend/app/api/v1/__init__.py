from fastapi import APIRouter

from app.api.v1.employees import router as employees_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(employees_router)
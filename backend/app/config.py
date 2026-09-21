from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_SQLITE = _BACKEND_ROOT / "data" / "salary.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ACME Salary Management API"
    # Local default: SQLite file (no Docker needed).
    # Later with Postgres: DATABASE_URL=postgresql://postgres:postgres@localhost:5433/salary_management
    database_url: str = f"sqlite:///{_DEFAULT_SQLITE}"
    cors_origins: str = "http://localhost:5173,http://localhost:8080"
    seed_employee_count: int = 10_000

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


settings = Settings()

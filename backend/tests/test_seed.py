from sqlalchemy import func, select

from app.models import Employee
from app.seed.seed_data import seed_employees


def test_seed_is_idempotent_for_small_batch(db):
    inserted = seed_employees(db, count=25, batch_size=10)
    assert inserted == 25
    total = db.scalar(select(func.count()).select_from(Employee))
    assert total == 25

    again = seed_employees(db, count=25)
    assert again == 0
    assert db.scalar(select(func.count()).select_from(Employee)) == 25

from decimal import Decimal

from app.models import Employee


def test_list_employees(client, employee):
    response = client.get("/api/v1/employees")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["employee_code"] == "E1001"


def test_list_employees_search(client, employee, db):
    other = Employee(
        employee_code="E2002",
        full_name="Alan Turing",
        email="alan@acme.test",
        country_code="GB",
        department="Research",
        job_title="Scientist",
        currency_code="GBP",
        annual_salary=Decimal("95000.00"),
        hire_date=employee.hire_date,
        is_active=True,
    )
    db.add(other)
    db.commit()

    response = client.get("/api/v1/employees", params={"q": "Turing"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["full_name"] == "Alan Turing"


def test_get_employee_detail(client, employee):
    response = client.get(f"/api/v1/employees/{employee.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "grace@acme.test"


def test_get_employee_not_found(client):
    response = client.get("/api/v1/employees/99999")
    assert response.status_code == 404


def test_patch_salary_and_history(client, employee):
    response = client.patch(
        f"/api/v1/employees/{employee.id}/salary",
        json={"annual_salary": "112500.00", "note": "Market adjustment"},
    )
    assert response.status_code == 200
    assert response.json()["annual_salary"] == "112500.00"

    history = client.get(f"/api/v1/employees/{employee.id}/salary-history")
    assert history.status_code == 200
    rows = history.json()
    assert len(rows) == 1
    assert rows[0]["old_salary"] == "100000.00"
    assert rows[0]["new_salary"] == "112500.00"
    assert rows[0]["note"] == "Market adjustment"


def test_patch_salary_validation(client, employee):
    response = client.patch(
        f"/api/v1/employees/{employee.id}/salary",
        json={"annual_salary": 0},
    )
    assert response.status_code == 422

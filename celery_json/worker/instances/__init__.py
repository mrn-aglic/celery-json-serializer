from celery_json.functions.helpers import example_function
from celery_json.models import Department, Employee

hr_department = Department(
    name="Human Resources",
    employees=[
        Employee(
            name="Alice",
            id=1,
            skills=["communication", "organization"],
        ),
        Employee(
            name="Bob",
            id=2,
            skills=["recruitment", "planning"],
        ),
    ],
    department_greeting=example_function,
    budget={"2023": 50000.00, "2024": 52000.00},
)

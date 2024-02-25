import json
import unittest
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from celery.schedules import crontab

from celery_json.encoder_decoder.encoder import CustomEncoder


@dataclass
class Employee:
    name: str
    id: int
    skills: List[str]
    employee_greeting: Optional[Callable] = None


@dataclass
class Department:
    name: str
    employees: List[Employee]
    budget: Dict[str, float]
    meeting_schedule: crontab = field(
        default_factory=lambda: crontab(minute="0", hour="9,17")
    )
    department_greeting: callable = field(default=lambda: "Welcome to the department")


# Example nested data classes
hr_department = Department(
    name="Human Resources",
    employees=[
        Employee(name="Alice", id=1, skills=["communication", "organization"]),
        Employee(name="Bob", id=2, skills=["recruitment", "planning"]),
    ],
    budget={"2023": 50000.00, "2024": 52000.00},
)


class TestComplexCustomEncoder(unittest.TestCase):
    def test_employee_serialization(self):
        employee = Employee("John", 3, ["Python", "Data Analysis"])
        expected = json.dumps(
            {
                "name": "John",
                "id": 3,
                "skills": ["Python", "Data Analysis"],
                "employee_greeting": None,
                "_type": "celery_json.test_encoder_decoder.encoder_tests.Employee",
            }
        )

        print(json.dumps(hr_department, cls=CustomEncoder))

        self.assertEqual(json.dumps(employee, cls=CustomEncoder), expected)

    def test_department_serialization(self):
        self.maxDiff = None

        expected = json.dumps(
            {
                "name": "Human Resources",
                "employees": [
                    {
                        "name": "Alice",
                        "id": 1,
                        "skills": ["communication", "organization"],
                        "employee_greeting": None,
                        "_type": "celery_json.test_encoder_decoder.encoder_tests.Employee",
                    },
                    {
                        "name": "Bob",
                        "id": 2,
                        "skills": ["recruitment", "planning"],
                        "employee_greeting": None,
                        "_type": "celery_json.test_encoder_decoder.encoder_tests.Employee",
                    },
                ],
                "budget": {"2023": 50000.00, "2024": 52000.00},
                "meeting_schedule": "<crontab: 0 9,17 * * * (m/h/dM/MY/d)>",
                "department_greeting": {
                    "name": "celery_json.test_encoder_decoder.encoder_tests.Department.<lambda>",
                    "args": [],
                    "kwargs": {},
                },
                "_type": "celery_json.test_encoder_decoder.encoder_tests.Department",
            }
        )

        print(type(json.dumps(hr_department, indent=4, cls=CustomEncoder)))
        with open("test.txt", "w") as f:
            json.dump(hr_department, fp=f, indent=4, cls=CustomEncoder)

        with open("test2.txt", "w") as f:
            json.dump(expected, fp=f, indent=4, cls=CustomEncoder)

        print(json.dumps(hr_department, indent=4, cls=CustomEncoder))

        print(type(expected))
        print(expected)

        self.assertEqual(json.dumps(hr_department, cls=CustomEncoder), expected)

    # Include previous test cases here for completeness


if __name__ == "__main__":
    unittest.main()

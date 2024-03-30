import json
import unittest

from celery_json.celery_json_serializer.serializer.decoder import CustomDecoder
from celery_json.functions.helpers import example_function
from celery_json.test_encoder_decoder.classes import Department, Employee

# Example nested data classes
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


class TestComplexCustomDecoder(unittest.TestCase):
    def test_employee_deserialization(self):
        expected = Employee(
            "John", 3, ["Python", "Data Analysis"], employee_greeting=example_function
        )

        employee = json.dumps(
            {
                "name": "John",
                "id": 3,
                "skills": ["Python", "Data Analysis"],
                "employee_greeting": {
                    "name": "celery_json.functions.helpers.example_function",
                    "args": [],
                    "kwargs": {},
                    "_handler": "FunctionHandler",
                },
                "_type": "celery_json.test_encoder_decoder.classes.Employee",
                "_handler": "DataclassHandler",
            }
        )

        self.assertEqual(json.loads(employee, cls=CustomDecoder), expected)

    def test_department_serialization(self):
        self.maxDiff = None

        expected = hr_department

        department = json.dumps(
            {
                "name": "Human Resources",
                "employees": [
                    {
                        "name": "Alice",
                        "id": 1,
                        "skills": ["communication", "organization"],
                        "employee_greeting": None,
                        "_type": "celery_json.test_encoder_decoder.classes.Employee",
                        "_handler": "DataclassHandler",
                    },
                    {
                        "name": "Bob",
                        "id": 2,
                        "skills": ["recruitment", "planning"],
                        "employee_greeting": None,
                        "_type": "celery_json.test_encoder_decoder.classes.Employee",
                        "_handler": "DataclassHandler",
                    },
                ],
                "budget": {"2023": 50000.00, "2024": 52000.00},
                "meeting_schedule": {
                    "month": {
                        "_result": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        "_handler": "SetHandler",
                    },
                    "day_of_month": {
                        "_result": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12,
                            13,
                            14,
                            15,
                            16,
                            17,
                            18,
                            19,
                            20,
                            21,
                            22,
                            23,
                            24,
                            25,
                            26,
                            27,
                            28,
                            29,
                            30,
                            31,
                        ],
                        "_handler": "SetHandler",
                    },
                    "day_of_week": {
                        "_result": [0, 1, 2, 3, 4, 5, 6],
                        "_handler": "SetHandler",
                    },
                    "hour": {
                        "_result": [9, 17],
                        "_handler": "SetHandler",
                    },
                    "minute": {
                        "_result": [0],
                        "_handler": "SetHandler",
                    },
                    "_handler": "CrontabHandler",
                },
                "department_greeting": {
                    "name": "celery_json.functions.helpers.example_function",
                    "args": [],
                    "kwargs": {},
                    "_handler": "FunctionHandler",
                },
                "_type": "celery_json.test_encoder_decoder.classes.Department",
                "_handler": "DataclassHandler",
            }
        )

        self.assertEqual(json.loads(department, cls=CustomDecoder), expected)

    # Include previous test cases here for completeness


if __name__ == "__main__":
    unittest.main()

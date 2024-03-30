from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from celery.schedules import crontab

from celery_json.celery_json_serializer import serializer_registration


@serializer_registration.register_dataclass
@dataclass
class Employee:
    name: str
    id: int
    skills: List[str]
    employee_greeting: Optional[Callable] = None


@serializer_registration.register_dataclass
@dataclass
class Department:
    name: str
    employees: List[Employee]
    budget: Dict[str, float]
    meeting_schedule: crontab = field(
        default_factory=lambda: crontab(minute="0", hour="9,17")
    )
    department_greeting: callable = field(default=lambda: "Welcome to the department")

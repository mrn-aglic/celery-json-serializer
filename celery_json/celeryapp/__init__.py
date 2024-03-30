import os

from celery import Celery

from . import celeryconfig
from .celeryconfig import task_queues
from .kombuconfig import register_serializer

register_serializer()

app = Celery("celery_json")

app.config_from_object(celeryconfig)

instance = os.environ.get("instance")

if instance == "scheduler":
    app.control.purge()

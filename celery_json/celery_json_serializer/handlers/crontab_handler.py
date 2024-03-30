from celery.schedules import crontab

from celery_json.celery_json_serializer.handlers.handler_base import (
    JsonHandler,
    wrap_handled_value,
)


class CrontabHandler(JsonHandler):
    def can_handle(self, obj):
        return isinstance(obj, crontab)

    @wrap_handled_value
    def encode(self, obj: crontab) -> dict:
        return {
            "month": obj.month_of_year,
            "day_of_month": obj.day_of_month,
            "day_of_week": obj.day_of_week,
            "hour": obj.hour,
            "minute": obj.minute,
        }

    def decode(self, obj: dict) -> crontab:
        month = obj["month"]
        day_of_month = obj["day_of_month"]
        day_of_week = obj["day_of_week"]
        hour = obj["hour"]
        minute = obj["minute"]

        return crontab(
            month_of_year=month,
            day_of_month=day_of_month,
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
        )

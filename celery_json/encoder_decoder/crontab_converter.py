from celery.schedules import crontab

from celery_json.encoder_decoder.converter import Converter


class CrontabConverter(Converter):
    @staticmethod
    def encode(obj: crontab) -> dict:
        return {
            "month": obj.month_of_year,
            "day_of_month": obj.day_of_month,
            "day_of_week": obj.day_of_week,
            "hour": obj.hour,
            "minute": obj.minute,
        }

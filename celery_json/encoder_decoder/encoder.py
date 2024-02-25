import functools
import json
from dataclasses import is_dataclass

from celery.schedules import crontab

from celery_json.encoder_decoder.crontab_converter import CrontabConverter
from celery_json.encoder_decoder.dataclass_converter import DataclassConverter
from celery_json.encoder_decoder.function_converter import FunctionConverter


# pylint: disable=no-else-return
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        is_partial = isinstance(obj, functools.partial)

        # Handle data classes
        if is_dataclass(obj):
            return DataclassConverter.encode(obj)

        # Handle functions by returning their name or a custom representation
        elif is_partial or isinstance(obj, type(lambda: None)):
            return FunctionConverter.encode(obj)
        # Handle nested custom objects by converting them to a dictionary
        # elif isinstance(obj, dict):
        #     return {k: self.default(v) for k, v in obj.__dict__.items() if not callable(v) and not k.startswith('__')}

        elif isinstance(obj, crontab):
            return CrontabConverter.encode(obj)

        return json.JSONEncoder.default(self, obj)
        # Add more cases here for other special types if necessary
        # return super().default(obj)

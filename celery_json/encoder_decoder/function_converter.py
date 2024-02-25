import functools

from celery_json.encoder_decoder.converter import Converter


class FunctionConverter(Converter):
    @staticmethod
    def encode(obj: callable) -> dict:
        is_partial = isinstance(obj, functools.partial)

        func = obj.func if is_partial else obj

        return {
            "name": f"{func.__module__}.{func.__qualname__}",
            "args": obj.args if is_partial else tuple(),
            "kwargs": obj.keywords if is_partial else {},
        }

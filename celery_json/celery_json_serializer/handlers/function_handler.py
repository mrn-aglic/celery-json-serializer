import functools
from typing import Callable

from celery_json.celery_json_serializer.handlers.handler_base import (
    JsonHandler,
    wrap_handled_value,
)


class FunctionHandler(JsonHandler):
    def __init__(self):
        super().__init__()

        self._func_mappings = {}

    def _get_func(self, obj):
        is_partial = isinstance(obj, functools.partial)

        return obj.func if is_partial else obj

    def get_func_name(self, func: functools.partial | Callable):
        func = self._get_func(func)
        return f"{func.__module__}.{func.__qualname__}"

    def register(self, func: functools.partial | Callable):
        name = self.get_func_name(func)

        self._func_mappings[name] = func
        # self._func_set.add(func)

    def _is_lambda(self, obj):
        func = self._get_func(obj)

        return hasattr(func, "__qualname__") and func.__qualname__ == "<lambda>"

    def can_handle(self, obj):
        return not self._is_lambda(obj) and isinstance(
            obj, (functools.partial, type(lambda: None))
        )

    @wrap_handled_value
    def encode(self, obj: callable) -> dict:
        is_partial = isinstance(obj, functools.partial)

        func_name = self.get_func_name(obj)

        return {
            "name": func_name,
            "args": obj.args if is_partial else tuple(),
            "kwargs": obj.keywords if is_partial else {},
        }

    def decode(self, obj: dict) -> functools.partial:
        name = obj["name"]
        args = obj["args"]
        kwargs = obj["kwargs"]

        func = self._func_mappings.get(name)

        if func is None:
            raise NotImplementedError(
                "Function not registered with this function handler"
            )

        if len(args) == 0 and not kwargs:
            return func

        return functools.partial(func, *args, **kwargs)

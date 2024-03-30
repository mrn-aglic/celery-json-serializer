import dataclasses
from typing import Callable, Type

from ..config.serialization_config import json_serialization_config
from ..handlers import DataclassHandler, FunctionHandler, JsonHandler


def _get_handler_instance(handler_class: Type[JsonHandler]) -> JsonHandler:
    handler_instance = json_serialization_config.get_handler_by_type(handler_class)
    return handler_instance if handler_instance is not None else handler_class()


def ensure_handler_registration(handler_class: Type[JsonHandler]) -> JsonHandler:
    handler_instance = _get_handler_instance(handler_class)

    json_serialization_config.register_handler(handler_instance)

    return handler_instance


def _wrapper(handler_instance: JsonHandler, to_register):
    handler_instance.register(to_register)


def register_function(func: Callable):
    handler_instance = ensure_handler_registration(FunctionHandler)

    _wrapper(handler_instance=handler_instance, to_register=func)

    return func


def register_dataclass(cls: dataclasses.dataclass):
    handler_instance = ensure_handler_registration(DataclassHandler)

    _wrapper(handler_instance=handler_instance, to_register=cls)

    return cls

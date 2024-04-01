import dataclasses
from typing import Callable, Optional, Type

from ..config.serialization_config import SerializationConfig, json_serialization_config
from ..handlers import DataclassHandler, FunctionHandler, JsonHandler


def _get_handler_instance(
    handler_class: Type[JsonHandler], config: SerializationConfig
) -> JsonHandler:
    handler_instance = config.get_handler_by_type(handler_class)

    return handler_instance if handler_instance is not None else handler_class()


def ensure_handler_registration(
    handler_class: Type[JsonHandler], config: SerializationConfig
) -> JsonHandler:
    handler_instance = _get_handler_instance(handler_class, config)

    config.register_handler(handler_instance)

    return handler_instance


def _wrapper(handler_instance: JsonHandler, to_register):
    handler_instance.register(to_register)


def register_function(
    func: Optional[Callable] = None, *, config: Optional[SerializationConfig] = None
) -> Callable:
    serialization_config = config or json_serialization_config

    def decorator(_func: Callable):
        handler_instance = ensure_handler_registration(
            FunctionHandler, serialization_config
        )

        _wrapper(handler_instance=handler_instance, to_register=_func)

        return _func

    if func is not None:
        return decorator(func)

    return decorator


def register_dataclass(
    cls: Optional[dataclasses.dataclass] = None,
    *,
    config: Optional[SerializationConfig] = None
) -> Callable:
    serialization_config = config or json_serialization_config

    def decorator(_cls: dataclasses.dataclass):
        handler_instance = ensure_handler_registration(
            DataclassHandler, serialization_config
        )

        _wrapper(handler_instance=handler_instance, to_register=_cls)

        return _cls

    if cls is not None:
        return decorator(cls)

    return decorator

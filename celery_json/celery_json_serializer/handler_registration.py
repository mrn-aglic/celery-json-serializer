from .config.serialization_config import json_serialization_config
from .handlers import CrontabHandler, DataclassHandler, FunctionHandler, SetHandler


def register_handlers():
    json_serialization_config.register_handler(DataclassHandler())
    json_serialization_config.register_handler(CrontabHandler())
    json_serialization_config.register_handler(FunctionHandler())
    json_serialization_config.register_handler(SetHandler())

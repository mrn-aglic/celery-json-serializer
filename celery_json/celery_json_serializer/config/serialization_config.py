from typing import Optional, Type

from ..handlers import JsonHandler


class SerializationConfig:
    def __init__(self):
        self._handlers = {}

    def register_handler(self, handler: JsonHandler):
        self._handlers[handler.__class__.__name__] = handler

    def get_handlers(self):
        return self._handlers.values()

    def get_handler(self, name: str) -> JsonHandler:
        return self._handlers[name]

    def get_handler_by_type(
        self, handler_cls: Type[JsonHandler]
    ) -> Optional[JsonHandler]:
        handler_name = handler_cls.__name__

        return self._handlers.get(handler_name)

    def has_handler(self, handler: Type[JsonHandler]) -> bool:
        return self.get_handler_by_type(handler) is not None


json_serialization_config = SerializationConfig()

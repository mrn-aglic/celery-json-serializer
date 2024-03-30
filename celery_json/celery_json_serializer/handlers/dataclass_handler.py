import dataclasses
from typing import Type

from celery_json.celery_json_serializer.handlers.handler_base import (
    JsonHandler,
    wrap_handled_value,
)


class DataclassHandler(JsonHandler):
    def __init__(self):
        super().__init__()

        self._dataclass_mapping = {}

    def can_handle(self, obj):
        return dataclasses.is_dataclass(obj)

    def register(self, dataclass: Type):
        name = f"{dataclass.__module__}.{dataclass.__name__}"
        self._dataclass_mapping[name] = dataclass

    def full_class_name(self, instance):
        return f"{instance.__class__.__module__}.{instance.__class__.__name__}"

    @wrap_handled_value
    def encode(self, obj, add_type: bool = True) -> dict:
        """Convert dataclass instance to a dictionary, including type information."""
        if not dataclasses.is_dataclass(obj):
            raise ValueError(
                "DataclassHandler.encode should only be called on dataclass instances."
            )

        # pylint: disable=no-else-return
        def convert(instance):
            if dataclasses.is_dataclass(instance):
                result = {
                    f.name: getattr(instance, f.name)
                    for f in dataclasses.fields(instance)
                }

                if add_type:
                    result["_type"] = self.full_class_name(instance)

                return result
            else:
                return instance

        return convert(obj)

    def decode(self, obj):
        name = obj["_type"]

        cls = self._dataclass_mapping[name]

        kwargs = self.drop_additional_keys(obj)

        instance = cls(**kwargs)

        return instance

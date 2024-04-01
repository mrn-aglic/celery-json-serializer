import json
from typing import Optional

from ..config.serialization_config import SerializationConfig, json_serialization_config


class CustomDecoder(json.JSONDecoder):
    _handler_key = "_handler"

    def __init__(self, *args, config: Optional[SerializationConfig], **kwargs):
        self.serialization_config = config or json_serialization_config

        super().__init__(object_hook=self.custom_decoding_hook, *args, **kwargs)

    # @staticmethod
    def custom_decoding_hook(self, obj):
        if CustomDecoder._handler_key in obj:
            handler_name = obj[CustomDecoder._handler_key]

            handler = self.serialization_config.get_handler(handler_name)
            return handler.decode(obj)

        return obj

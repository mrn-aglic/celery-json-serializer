import json
from typing import Optional

from ..config.serialization_config import SerializationConfig, json_serialization_config


class CustomEncoder(json.JSONEncoder):
    def __init__(self, *args, config: Optional[SerializationConfig] = None, **kwargs):
        self.serialization_config = config or json_serialization_config

        super().__init__(*args, **kwargs)

    def default(self, obj):
        for handler in self.serialization_config.get_handlers():
            if handler.can_handle(obj):
                result = handler.encode(obj)
                return result

        return json.JSONEncoder.default(self, obj)

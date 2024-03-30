import json

from ..config.serialization_config import json_serialization_config


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        for handler in json_serialization_config.get_handlers():
            if handler.can_handle(obj):
                result = handler.encode(obj)
                return result

        return json.JSONEncoder.default(self, obj)

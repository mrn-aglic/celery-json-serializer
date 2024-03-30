from celery_json.celery_json_serializer.handlers.handler_base import (
    JsonHandler,
    wrap_handled_value,
)


class SetHandler(JsonHandler):
    def can_handle(self, obj):
        """Return True if this handler can handle the object."""
        return isinstance(obj, set)

    @wrap_handled_value
    def encode(self, obj):
        """Encode the object."""
        return list(obj)

    def decode(self, obj: dict) -> set:
        return set(obj["_result"])

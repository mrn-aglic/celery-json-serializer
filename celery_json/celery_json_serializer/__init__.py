import json

from .callable_registration import registration as serializer_registration
from .config import json_serialization_config
from .handler_registration import register_handlers
from .serializer.decoder import CustomDecoder
from .serializer.encoder import CustomEncoder


def celery_encoder(obj):
    return json.dumps(obj, cls=CustomEncoder)


def celery_decoder(obj):
    return json.loads(obj, cls=CustomDecoder)


register_handlers()

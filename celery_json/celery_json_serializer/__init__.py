import json

from .callable_registration import registration as serializer_registration
from .config import SerializationConfig, json_serialization_config
from .handler_registration import register_handlers
from .serializer.decoder import CustomDecoder
from .serializer.encoder import CustomEncoder


def get_custom_config_celery_encoder(config: SerializationConfig):
    def _encoder(obj):
        return json.dumps(obj, cls=CustomEncoder, config=config)

    return _encoder


def get_custom_config_celery_decoder(config: SerializationConfig):
    def _decoder(obj):
        return json.loads(obj, cls=CustomDecoder, config=config)

    return _decoder


def celery_encoder(obj):
    return json.dumps(obj, cls=CustomEncoder, config=json_serialization_config)


def celery_decoder(obj):
    return json.loads(obj, cls=CustomDecoder, config=json_serialization_config)


register_handlers()

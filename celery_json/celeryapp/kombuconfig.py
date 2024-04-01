from kombu.serialization import register

from celery_json.celery_json_serializer import (
    SerializationConfig,
    celery_decoder,
    celery_encoder,
    get_custom_config_celery_decoder,
    get_custom_config_celery_encoder,
)
from celery_json.celery_json_serializer.handlers import SetHandler


def register_serializer():
    register(
        name="custom_json_serializer",
        encoder=celery_encoder,
        decoder=celery_decoder,
        content_type="application/json",
    )


# An example of how to provide a custom configuration to the serializer
def register_custom_config_serializer():
    config = SerializationConfig()
    config.register_handler(SetHandler())

    encoder = get_custom_config_celery_encoder(config=config)
    decoder = get_custom_config_celery_decoder(config=config)

    register(
        name="custom_json_serializer",
        encoder=encoder,
        decoder=decoder,
        content_type="application/json",
    )

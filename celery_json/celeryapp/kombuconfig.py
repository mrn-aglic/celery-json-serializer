from kombu.serialization import register

from celery_json.celery_json_serializer import celery_decoder, celery_encoder


def register_serializer():
    register(
        name="custom_json_serializer",
        encoder=celery_encoder,
        decoder=celery_decoder,
        content_type="application/json",
    )

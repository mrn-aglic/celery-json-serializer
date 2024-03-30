from celery_json.celery_json_serializer import serializer_registration


@serializer_registration.register_function
def example_function():
    print("hello from example function")

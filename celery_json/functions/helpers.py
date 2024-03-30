from celery_json.celery_json_serializer.callable_registration import (
    registration as json_function_registration,
)


@json_function_registration.register_function
def example_function():
    print("hello from example function")

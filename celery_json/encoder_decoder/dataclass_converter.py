import dataclasses

from celery_json.encoder_decoder.converter import Converter


def full_class_name(instance):
    return f"{instance.__class__.__module__}.{instance.__class__.__name__}"


class DataclassConverter(Converter):
    @staticmethod
    def encode(obj, add_type: bool = True) -> dict:
        """Convert dataclass instance to a dictionary, including type information."""
        if not dataclasses.is_dataclass(obj):
            raise ValueError(
                "custom_asdict() should only be called on dataclass instances."
            )

        # pylint: disable=no-else-return
        def convert(instance):
            if dataclasses.is_dataclass(instance):
                result = {
                    f.name: convert(getattr(instance, f.name))
                    for f in dataclasses.fields(instance)
                }
                if add_type:
                    result["_type"] = full_class_name(instance)
                return result
            elif isinstance(instance, (list, tuple)):
                return type(instance)(convert(item) for item in instance)
            elif isinstance(instance, dict):
                return {key: convert(value) for key, value in instance.items()}
            else:
                return instance

        return convert(obj)

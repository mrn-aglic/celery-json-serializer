import abc
from typing import Callable


def wrap_handled_value(func) -> callable:
    def wrapper(*args, **kwargs):
        self = args[0]

        if not isinstance(self, JsonHandler):
            raise TypeError("Wrapper needs to be used on JsonHandler instance")

        func_return_value = func(*args, **kwargs)

        if isinstance(func_return_value, dict):
            return {**func_return_value, "_handler": self.__class__.__name__}

        return {"_result": func_return_value, "_handler": self.__class__.__name__}

    return wrapper


def unwrap_handled_value(func) -> callable:
    def wrapper(*args, **kwargs):
        self = args[0]

        if not isinstance(self, JsonHandler):
            raise TypeError("Wrapper needs to be used on JsonHandler instance")

        func_return_value = func(*args, **kwargs)

        if isinstance(func_return_value, dict):
            return {**func_return_value, "_handler": self.__class__.__name__}

        return {"_result": func_return_value, "_handler": self.__class__.__name__}

    return wrapper


class JsonHandler(abc.ABC):
    _type_key = "_type"

    @abc.abstractmethod
    def can_handle(self, obj):
        """Return True if this handler can handle the object."""
        raise NotImplementedError

    @abc.abstractmethod
    def encode(self, obj):
        """Encode the object."""
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, obj):
        """Decode the obj."""
        raise NotImplementedError

    def drop_additional_keys(self, obj):
        if not isinstance(obj, dict):
            return obj

        new_dict = {**obj}

        new_dict.pop("_type")
        new_dict.pop("_handler")

        return new_dict

    def register(self, callable_type: Callable):
        pass

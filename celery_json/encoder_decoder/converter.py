from abc import ABC
from typing import Any


class Converter(ABC):
    @staticmethod
    def encode(obj: Any) -> dict:
        pass

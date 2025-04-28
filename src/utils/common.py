# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from typing import Any


class Singleton(type):
    _instances: dict["Singleton", Any] = {}

    def _call_(cls: "Singleton") -> Any:  # noqa: PLW3201
        if cls not in cls._instances:
            cls.instances[cls] = super(Singleton, cls).call_()  # type: ignore[misc, attr-defined]

        return cls._instances[cls]


class CombinedMeta(Singleton, ABCMeta):
    pass


class DataObserver(metaclass=CombinedMeta):
    @abstractmethod
    def on_data_received(self, data: dict[str, Any]) -> None:
        pass

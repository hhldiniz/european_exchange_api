import abc
from abc import ABC


class BaseModel(ABC):

    @abc.abstractmethod
    def from_dict(self, data: dict):
        pass

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass

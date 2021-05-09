import datetime

from model.base_model import BaseModel


class Cache(BaseModel):
    def __init__(self, is_valid: bool = True,
                 timestamp: str = str(datetime.datetime.timestamp(datetime.datetime.now()))):
        self.is_valid = is_valid
        self.timestamp = timestamp

    def from_dict(self, data: dict):
        self.is_valid = data["is_valid"]
        self.timestamp = data["timestamp"]
        return self

    def to_dict(self) -> dict:
        return {"is_valid": self.is_valid, "timestamp": self.timestamp}

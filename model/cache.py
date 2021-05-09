import datetime

from model.base_model import BaseModel


class Cache(BaseModel):
    def __init__(self, is_valid: bool = True,
                 timestamp: str = str(datetime.datetime.timestamp(datetime.datetime.now()))):
        self.is_valid = is_valid
        self.timestamp = timestamp

    def from_dict(self, data: dict):
        return Cache(data["is_valid"], data["timestamp"])

    def to_dict(self) -> dict:
        return {"is_valid": self.is_valid, "timestamp": self.timestamp}

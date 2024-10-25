import json

from model.base_model import BaseModel


class Currency(BaseModel):
    def __init__(self, currency_code: str = "", rate: float = 0, historical_date: str = "", timestamp: float = 0,
                 friendly_name: str = ""):
        self.currency_code = currency_code
        self.rate = rate
        self.historical_date = historical_date
        self.timestamp = timestamp
        self.friendly_name = friendly_name

    def to_dict(self) -> dict:
        return {'currency_code': self.currency_code, 'rate': self.rate, 'historical_date': self.historical_date,
                'timestamp': self.timestamp, 'friendly_name': self.friendly_name}

    def from_dict(self, data: dict):
        self.__validate_dict(data)
        self.currency_code = data["currency_code"]
        self.rate = data["rate"]
        self.historical_date = data["historical_date"]
        self.timestamp = data["timestamp"]
        self.friendly_name = data["friendly_name"]
        return self

    @staticmethod
    def __validate_dict(data: dict):
        if not ("currency_code" in data
                or "rate" in data
                or "historical_date" in data
                or "timestamp" in data
                or "friendly_name" in data):
            raise ValueError(
                f"Dict doesn't contain all the information needed to parse as Currency model. Current dict: {data}")

    def __str__(self):
        return self.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

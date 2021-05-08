from model.base_model import BaseModel


class Currency(BaseModel):
    def __init__(self, currency_code: str, value: float, historical_date: str, timestamp: str, friendly_name: str):
        self.currency_code = currency_code
        self.value = value
        self.historical_date = historical_date
        self.timestamp = timestamp
        self.friendly_name = friendly_name

    def to_dict(self) -> dict:
        return {'currency_cod': self.currency_code, 'value': self.value, 'historical_date': self.historical_date,
                'timestamp': self.timestamp, 'friendly_name': self.friendly_name}

    @staticmethod
    def from_dict(data: dict):
        return Currency(data["currency_code"], data["value"], data["historical_date"], data["timestamp"],
                        data["friendly_name"])

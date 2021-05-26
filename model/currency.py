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
        self.currency_code = data["currency_code"]
        self.rate = data["rate"]
        self.historical_date = data["historical_date"]
        self.timestamp = data["timestamp"]
        self.friendly_name = data["friendly_name"]
        return self

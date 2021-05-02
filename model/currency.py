class Currency:
    def __init__(self, currency_code: str, value: float, historical_date: str, timestamp: str, friendly_name: str):
        self.currency_code = currency_code
        self.value = value
        self.historicalDate = historical_date
        self.timestamp = timestamp
        self.friendly_name = friendly_name

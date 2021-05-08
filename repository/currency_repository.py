from dao.currency_dao import CurrencyDao
from model.currency import Currency


class CurrencyRepository:
    def __init__(self):
        self._currency_dao = CurrencyDao()

    def get_all(self) -> [Currency]:
        self._currency_dao.select({})

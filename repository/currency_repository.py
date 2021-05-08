from dao.currency_dao import CurrencyDao
from model.currency import Currency


class CurrencyRepository:
    def __init__(self):
        self._currency_dao = CurrencyDao()

    def get_all(self) -> [Currency]:
        self._currency_dao.select({})

    def insert(self, *currency):
        self._currency_dao.insert(*currency)

    def delete(self, *currency):
        self._currency_dao.delete(*currency)

    def select_one(self, ftr: dict) -> Currency:
        return self._currency_dao.select(ftr)

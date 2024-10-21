import unittest
from datetime import datetime
from unittest.mock import MagicMock

from pymongo.results import InsertOneResult, DeleteResult

from terraform.project_dependencies.common.python.model.currency import Currency
from terraform.project_dependencies.common.python.repository.currency_repository import CurrencyRepository


class TestCurrencyData(unittest.TestCase):

    def setUp(self) -> None:
        self.currency_repository = CurrencyRepository()
        self.mock_currency = Currency(
            "USD",
            1,
            "2020-01-01",
            datetime.timestamp(datetime.now()),
            "American Dolar"
        )
        self.currency_repository.insert = MagicMock(return_value=InsertOneResult(1, True))
        self.currency_repository.delete = MagicMock(return_value=DeleteResult({"1": ""}, True))
        self.currency_repository.select_one = MagicMock(return_value=self.mock_currency)

    def test_currency_insert(self):
        assert isinstance(self.currency_repository.insert(self.mock_currency), InsertOneResult)
        assert isinstance(self.currency_repository.delete(self.mock_currency), DeleteResult)

    def test_currency_select(self):
        self.currency_repository.insert(self.mock_currency)
        res = self.currency_repository.select_one({'currency_code': self.mock_currency.currency_code})
        self.currency_repository.delete(self.mock_currency)
        assert isinstance(res, Currency)

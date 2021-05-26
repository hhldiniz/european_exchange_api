from datetime import datetime

from model.currency import Currency
from repository.currency_repository import CurrencyRepository

mock_currency = Currency(
        "USD",
        1,
        "2020-01-01",
        str(datetime.timestamp(datetime.now())),
        "American Dolar"
    )
currency_repository = CurrencyRepository()


def test_currency_insert():
    currency_repository.insert(mock_currency)
    currency_repository.delete(mock_currency)


def test_currency_select():
    currency_repository.insert(mock_currency)
    res = currency_repository.select_one({'currency_code': mock_currency.currency_code})
    currency_repository.delete(mock_currency)
    assert isinstance(res, Currency)

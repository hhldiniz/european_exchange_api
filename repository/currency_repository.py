import datetime
import xml.etree.ElementTree as elementTree
from typing import Generator
from xml.etree import ElementTree

import pymongo
from requests import get

import constants
from dao.currency_dao import CurrencyDao
from logger import Logger
from model.currency import Currency
from repository.cache_repository import CacheRepository


class CurrencyRepository:
    def __init__(self):
        self._currency_dao = CurrencyDao()
        self._cache_repository = CacheRepository()

    @staticmethod
    def _request_remote_data() -> ElementTree:
        Logger.i("CurrencyRepository#_request_remote_data -> Requesting remote data")
        res = get(constants.history_all_time_url)
        Logger.i("CurrencyRepository#_request_remote_data -> Remote data requested")
        return elementTree.fromstring(res.content.decode("utf-8"))

    @staticmethod
    def _parse_xml_content(content: ElementTree) -> [Currency]:
        Logger.i("CurrencyRepository#_parse_xml_content -> Beginning xml parsing")
        currency_list = []
        for item in content.iter():
            time = item.get("time")
            if time is not None:
                for currency_xml_obj in item:
                    currency = Currency()
                    currency_code = currency_xml_obj.get("currency")
                    rate = currency_xml_obj.get("rate")
                    if time is not None:
                        currency.historical_date = time
                    if currency_code is not None:
                        currency.currency_code = currency_code
                    if rate is not None:
                        currency.rate = float(rate)
                    currency.timestamp = datetime.datetime.timestamp(datetime.datetime.now())
                    currency.friendly_name = currency_code
                    currency_list.append(currency)
        Logger.i("CurrencyRepository#_parse_xml_content -> Xml parsing completed")
        return currency_list

    @staticmethod
    def __filter_local_list(currency_data: [Currency], start_at: [str, None], end_at: [str, None],
                            symbols: [[str], None]) -> [Currency]:
        currencies_as_string = str(currency_data)
        Logger.i(
            f"CurrencyRepository#__filter_local_list -> Applying local data filter with params: "
            f"start_at = {start_at}, end_at = {end_at}, symbols = {symbols}")
        print(currencies_as_string)

        def check_currency(currency: Currency) -> bool:
            symbols_condition = currency.currency_code in symbols if symbols else True
            start_at_condition = datetime.datetime.strptime(currency.historical_date, "%Y-%M-%d"
                                                            ) >= datetime.datetime.strptime(start_at, "%Y-%M-%d"
                                                                                            ) if start_at else True
            end_at_condition = datetime.datetime.strptime(currency.historical_date, "%Y-%M-%d") <= datetime. \
                datetime.strptime(end_at, "%Y-%M-%d") if end_at else True
            return symbols_condition and start_at_condition and end_at_condition

        Logger.i("CurrencyRepository#__filter_local_list -> Local data filter complete")
        return list(filter(lambda currency: check_currency(currency), currency_data))

    def _verify_and_update_cache(self) -> tuple[bool, [list, None]]:
        Logger.i("CurrencyRepository#_verify_and_update_cache -> Checking cache data")
        if not self._cache_repository.get_valid_cache().is_valid:
            currency_data = self._parse_xml_content(self._request_remote_data())
            self._cache_repository.update_cache()
            self._currency_dao.insert(*currency_data)
            Logger.i("CurrencyRepository#_verify_and_update_cache -> Cache is valid")
            return True, currency_data
        Logger.i("CurrencyRepository#_verify_and_update_cache -> Cache is invalid")
        return False, None

    @staticmethod
    def normalize_by_base(base_currency_code: str, currency_data: [Currency]) -> Generator[Currency, None, None]:
        Logger.i(f"CurrencyRepository#_verify_and_update_cache -> Normalizing currency data with params: "
                 f"base_currency_code = {base_currency_code}, currency_data = {currency_data}")
        base_currency = list(filter(lambda l_currency: l_currency.currency_code == base_currency_code, currency_data))[
            0]
        for currency in currency_data:
            currency.rate = currency.rate / base_currency.rate
            yield currency
        Logger.i("CurrencyRepository#_verify_and_update_cache -> Currency data normalized")

    def get_all(self, base_currency_code: str, start_at: [str, None], end_at: [str, None], symbols: [[str], None]) -> \
            [Currency]:
        base_currency_code = base_currency_code.upper()

        cache = self._verify_and_update_cache()

        if cache[0]:
            Logger.i("CurrencyRepository#get_all -> Retrieving data remotely with params: ")
            Logger.i(f"base_currency_code = {base_currency_code}, "
                     f"start_at = {start_at}, end_at = {end_at}, symbols = {symbols}")
            return self.__filter_local_list(list(self.normalize_by_base(base_currency_code, cache[1])), start_at,
                                            end_at, symbols)
        else:
            Logger.i("CurrencyRepository#get_all -> Retrieving data locally")
            Logger.i(f"base_currency_code = {base_currency_code}, "
                     f"start_at = {start_at}, end_at = {end_at}, symbols = {symbols}")
            filters = {}
            if start_at:
                filters['start_at'] = {'$gte': start_at}
            if end_at:
                filters['end_at'] = {'$lte': end_at}
            if symbols:
                filters['symbols'] = {'$in': symbols}
            return self._currency_dao.select_many(filters)

    def get_latest(self, symbol: str) -> Currency:
        cache = self._verify_and_update_cache()
        if cache[0]:
            Logger.i(f"CurrencyRepository#latest -> Retrieving data remotely with params: symbol = {symbol}")
            return self.__filter_local_list(cache[1],
                                            (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%M-%d"),
                                            datetime.datetime.now().strftime("%Y-%M-%d"), [symbol])[0]
        else:
            Logger.i(f"CurrencyRepository#latest -> Retrieving data locally with params: symbol = {symbol}")
            return self._currency_dao.select_one({"symbols": symbol}, ("historical_data", pymongo.DESCENDING))

    def insert(self, *currency):
        Logger.i(f"CurrencyRepository#insert -> Inserting objects: {[*currency]}")
        self._currency_dao.insert(*currency)

    def delete(self, *currency):
        Logger.i(f"CurrencyRepository#delete -> Deleting objects: {[*currency]}")
        self._currency_dao.delete(*currency)

    def select_one(self, ftr: dict) -> Currency:
        Logger.i(f"CurrencyRepository#select_one -> Retrieving one object with filter {ftr}")
        return self._currency_dao.select_one(ftr)

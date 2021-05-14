import datetime
import os
from xml.etree import ElementTree

from pandas import DataFrame
from sklearn import preprocessing

from dao.currency_dao import CurrencyDao
from exceptions.no_cache_available_exception import NoCacheAvailableException
from model.currency import Currency
from requests import get
import xml.etree.ElementTree as elementTree

import constants
from repository.cache_repository import CacheRepository


class CurrencyRepository:
    def __init__(self):
        self._currency_dao = CurrencyDao()
        self._cache_repository = CacheRepository()

    @staticmethod
    def _request_remote_data() -> ElementTree:
        xml_file_path = os.path.join(constants.APP_ROOT, "history/static/content.xml")
        try:
            xml_file = open(xml_file_path, "r")
        except FileNotFoundError:
            xml_file = open(xml_file_path, "w")
            res = get(constants.history_all_time_url)
            xml_file.write(res.content.decode("utf-8"))
        return elementTree.parse(xml_file)

    @staticmethod
    def _parse_xml_content(content: ElementTree) -> [Currency]:
        currency_list = []

        for item in content.getroot().iter():
            currency = Currency()
            time = item.get("time")
            currency_code = item.get("currency")
            rate = item.get("rate")
            if time is not None:
                currency.historical_date = time
            if currency_code is not None:
                currency.currency_code = currency_code
            if rate is not None:
                currency.rate = rate
            currency.timestamp = datetime.datetime.timestamp(datetime.datetime.now())
            currency_list.append(currency)
        return currency_list

    @staticmethod
    def _populate_dataframe(currency_list: [Currency]) -> DataFrame:
        return DataFrame(list(map(lambda currency: currency.to_dict(), currency_list)))

    def get_all(self, base_currency_code: str) -> [Currency]:
        base_currency_code = base_currency_code.upper()

        try:
            if not self._cache_repository.get_valid_cache().is_valid:
                currency_data = self._parse_xml_content(self._request_remote_data())
                currency_data_frame = self._populate_dataframe(currency_data)
                self._update_cache_data(currency_data)
                return currency_data_frame
            else:
                return self._currency_dao.select_many({})
        except NoCacheAvailableException:
            currency_data = self._parse_xml_content(self._request_remote_data())
            self._update_cache_data(currency_data)
            currency_data_frame = self._populate_dataframe(currency_data)
            return currency_data_frame

    def _update_cache_data(self, currency_data: [Currency]):
        self._cache_repository.update_cache()
        self._currency_dao.insert(*currency_data)

    def insert(self, *currency):
        self._currency_dao.insert(*currency)

    def delete(self, *currency):
        self._currency_dao.delete(*currency)

    def select_one(self, ftr: dict) -> Currency:
        return self._currency_dao.select_one(ftr)

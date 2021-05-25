import datetime
import os
import xml.etree.ElementTree as elementTree
from collections import Generator
from xml.etree import ElementTree

from requests import get

import constants
from dao.currency_dao import CurrencyDao
from model.currency import Currency
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
        return currency_list

    def get_all(self, base_currency_code: str) -> [Currency]:
        base_currency_code = base_currency_code.upper()

        if not self._cache_repository.get_valid_cache().is_valid:
            currency_data = self._parse_xml_content(self._request_remote_data())
            self._update_cache_data(currency_data)
            return list(self.normalize_by_base(base_currency_code, currency_data))
        else:
            data = self._currency_dao.select_many({})
            return list(map(lambda currency_dict: Currency().from_dict(currency_dict), data))

    @staticmethod
    def normalize_by_base(base_currency_code: str, currency_data: [Currency]) -> Generator[Currency]:
        base_currency = list(filter(lambda l_currency: l_currency.currency_code == base_currency_code, currency_data))[
            0]
        for currency in currency_data:
            currency.rate = currency.rate / base_currency.rate
            yield currency

    def _update_cache_data(self, currency_data: [Currency]):
        self._cache_repository.update_cache()
        self._currency_dao.insert(*currency_data)

    def insert(self, *currency):
        self._currency_dao.insert(*currency)

    def delete(self, *currency):
        self._currency_dao.delete(*currency)

    def select_one(self, ftr: dict) -> Currency:
        return self._currency_dao.select_one(ftr)

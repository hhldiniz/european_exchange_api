import datetime
import os
from xml.etree import ElementTree

from pandas import DataFrame

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

    def get_all(self, base_currency_code: str) -> [Currency]:
        base_currency_code = base_currency_code.upper()
        currency_data = DataFrame()

        def request_remote_data() -> ElementTree:
            xml_file_path = os.path.join(constants.APP_ROOT, "history/static/content.xml")
            try:
                xml_file = open(xml_file_path, "r")
            except FileNotFoundError:
                xml_file = open(xml_file_path, "w")
                res = get(constants.history_all_time_url)
                xml_file.write(res.content.decode("utf-8"))
            return elementTree.parse(xml_file)

        def parse_xml_content(content: ElementTree) -> [Currency]:
            for item in content.getroot().find("Cube").findall("Cube"):
                historical_date = item.get("time")
                for subItem in item.findall("Cube"):
                    currency = Currency()
                    currency.currency_code = subItem.get("currency")
                    currency.historical_date = historical_date
                    currency.timestamp = datetime.datetime.timestamp(datetime.datetime.now())
                    currency.rate = subItem.get("rate")
                    currency_data.append(currency.to_dict())

        cache_repository = CacheRepository()
        try:
            if not cache_repository.get_valid_cache().is_valid:
                return parse_xml_content(request_remote_data())
            else:
                return self._currency_dao.select_many({})
        except NoCacheAvailableException:
            return parse_xml_content(request_remote_data())

    def insert(self, *currency):
        self._currency_dao.insert(*currency)

    def delete(self, *currency):
        self._currency_dao.delete(*currency)

    def select_one(self, ftr: dict) -> Currency:
        return self._currency_dao.select_one(ftr)

from datetime import datetime

from dao.cache_dao import CacheDao
from exceptions.no_cache_available_exception import NoCacheAvailableException
from model.cache import Cache


class CacheRepository:
    def __init__(self):
        self._cache_dao = CacheDao()

    def get_valid_cache(self) -> Cache:
        try:
            last_available_cache = self._cache_dao.select_one({'is_valid': True})
            if datetime.fromtimestamp(
                    datetime.timestamp(datetime.now()) - last_available_cache.timestamp).time().hour > 1:
                last_available_cache.is_valid = False
                self._cache_dao.update(last_available_cache)
            return last_available_cache
        except TypeError:
            raise NoCacheAvailableException

    def update_cache(self):
        self._cache_dao.insert(Cache())

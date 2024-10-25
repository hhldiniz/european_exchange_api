from datetime import datetime

from dao.cache_dao import CacheDao
from model.cache import Cache


class CacheRepository:
    def __init__(self):
        self._cache_dao = CacheDao()

    def get_valid_cache(self) -> Cache:
        last_available_cache = self._cache_dao.select_one({'is_valid': True})
        if last_available_cache is not None:
            if datetime.fromtimestamp(
                    datetime.timestamp(datetime.now()) - last_available_cache.timestamp).time().hour > 1:
                last_available_cache.is_valid = False
                self._cache_dao.update(last_available_cache)
            return last_available_cache
        else:
            return Cache()

    def update_cache(self):
        self._cache_dao.insert(Cache())

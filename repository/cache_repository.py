from dao.cache_dao import CacheDao
from exceptions.no_cache_available_exception import NoCacheAvailableException
from model.cache import Cache


class CacheRepository:
    def __init__(self):
        self._cache_dao = CacheDao()

    def get_valid_cache(self) -> Cache:
        try:
            return self._cache_dao.select_one({'is_valid': True})
        except KeyError:
            raise NoCacheAvailableException

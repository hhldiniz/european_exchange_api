from dao.base_dao import BaseDao
from model.cache import Cache


class CacheDao(BaseDao):
    def __init__(self):
        super().__init__()

    def insert(self, *cache: Cache):
        if cache.__len__() == 1:
            self.db_connection.insert_one(self.table, cache[0].to_dict())
        elif cache.__len__() > 1:
            self.db_connection.insert_many(self.table, list(map(lambda this_cache: this_cache.to_dict(), cache)))
        else:
            print("CacheDao#insert: Nothing to insert")

    def delete(self, *cache: Cache):
        if cache.__len__() == 1:
            self.db_connection.delete_one(self.table,
                                          {"is_valid": cache[0].is_valid, "timestamp": cache[0].timestamp})
        elif cache.__len__() > 1:
            self.db_connection.delete_many(self.table, {'timestamp': {
                "$set": list(map(lambda this_cache: this_cache.timestamp, cache))}})

    def update(self, *cache: Cache):
        if cache.__len__() > 0:
            self.db_connection.update_many(self.table, {
                'timestamp': list(map(lambda this_cache: this_cache.timestamp, cache))})
        else:
            print("CacheDao#update: Nothing to update")

    def select_one(self, ftr: dict) -> Cache:
        cache = self.db_connection.select_one(self.table, ftr)
        return Cache().from_dict(cache) if cache is not None else Cache()

    def select_many(self, ftr: dict) -> [Cache]:
        return list(map(lambda obj: Cache(obj["is_valid"], obj["timestamp"]),
                        self.db_connection.select_many(self.table, ftr)))

    @property
    def schema(self) -> dict:
        return {
            "is_valid": {
                "required": True,
            },
            "timestamp": {
                "unique": True,
                "required": True
            }
        }

    @property
    def table(self) -> str:
        return "cache"

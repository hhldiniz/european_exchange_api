from dao.base_dao import BaseDao
from model.cache import Cache


class CacheDao(BaseDao):
    def __init__(self):
        super().__init__()

    def insert(self, *cache: Cache):
        if cache.__len__() == 1:
            self.db_connection.insert(self.collection(), cache[0].to_dict())
        elif cache.__len__() > 1:
            self.db_connection.insert_many(self.collection(), list(map(lambda this_cache: this_cache.to_dict(), cache)))
        else:
            print("CacheDao#insert: Nothing to insert")

    def delete(self, *cache: Cache):
        pass

    def update(self, *cache: Cache):
        pass

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

    def collection(self) -> str:
        return "cache"

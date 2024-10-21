import pymongo
from pymongo import MongoClient

from common.python.util.providers.base_database_provider import BaseDatabaseProvider


class LocalDatabaseProvider(BaseDatabaseProvider):
    def get_connection(self) -> MongoClient:
        connection = pymongo.MongoClient("mongodb://localhost:27017/euroapi")
        return connection

import pymongo
from pymongo import MongoClient

from config import Config
from util.providers.base_database_provider import BaseDatabaseProvider


class RemoteDatabaseProvider(BaseDatabaseProvider):
    def get_connection(self) -> MongoClient:
        connection = pymongo.MongoClient(
            f"mongodb+srv://{Config.DB_USER.value}:{Config.DB_PASSWORD.value}@exhange-api-cluster.9wao9.mongodb.net/"
            f"?retryWrites=true&w=majority&appName=exhange-api-cluster")
        return connection

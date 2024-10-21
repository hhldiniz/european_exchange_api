import pymongo
from pymongo import MongoClient

from terraform.project_dependencies.common.python.config import Config
from terraform.project_dependencies.common.python.util.providers.base_database_provider import BaseDatabaseProvider


class RemoteDatabaseProvider(BaseDatabaseProvider):
    def get_connection(self) -> MongoClient:
        connection = pymongo.MongoClient(
            f"mongodb+srv://{Config.DB_USER.value}:{Config.DB_PASSWORD.value}@exhange-api-cluster.yufz9.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority")
        return connection


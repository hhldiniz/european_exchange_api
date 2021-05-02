import pymongo

from database_access import DB_USER, DB_PASSWORD, DB_NAME
from util.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.__connection = pymongo.MongoClient(
            f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@exhange-api-cluster.yufz9.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority")
        self.__database = self.__connection.get_database(DB_NAME)

    def insert(self, collection: str, data: dict):
        self.__database.get_collection(collection).insert(data)

    def update_one(self, collection: str, condition: dict, data: dict):
        self.__database.get_collection(collection).replace_one(condition, data)

    def update_many(self, collection: str, condition: dict, data: dict):
        self.__database.get_collection(collection).replace_one(condition, data)

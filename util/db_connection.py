import pymongo

from database_access import DB_USER, DB_PASSWORD, DB_NAME, DbInstance
from util.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.__connection = pymongo.MongoClient(
            f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@exhange-api-cluster.yufz9.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority" if DbInstance is DbInstance.REMOTE else
            f"mongodb://localhost:27017/euroapi")
        self.__database = self.__connection.get_database(DB_NAME)

    def insert(self, collection: str, data: dict):
        self.__database.get_collection(collection).insert_one(data)

    def insert_many(self, collection: str, data: [dict]):
        self.__database.get_collection(collection).insert_many(data)

    def update_one(self, collection: str, condition: dict, data: dict):
        self.__database.get_collection(collection).replace_one(condition, data)

    def update_many(self, collection: str, condition: dict, data: dict):
        self.__database.get_collection(collection).update_many(condition, data)

    def delete_one(self, collection: str, ftr: dict):
        self.__database.get_collection(collection).delete_one(ftr)

    def delete_many(self, collection: str, ftr: dict):
        self.__database.get_collection(collection).delete_many(ftr)

    def select_one(self, collection: str, ftr: dict) -> dict:
        return self.__database.get_collection(collection).find_one(ftr)

    def select_many(self, collection: str, ftr: dict) -> [dict]:
        return self.__database.get_collection(collection).find(ftr)

    def create_collection(self, collection: str):
        self.__database.create_collection(collection)

    def run_command(self, command: dict):
        self.__database.command(command)

    def find_and_update(self, collection: str, condition: dict, data: dict):
        self.__database.get_collection(collection).find_one_and_update(condition, data)

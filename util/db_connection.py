import pymongo

from config import Config
from util.server_env import ServerEnv
from util.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.__connection = pymongo.MongoClient(
            f"mongodb+srv://{Config.DB_USER.value   }:{Config.DB_PASSWORD.value}@exhange-api-cluster.yufz9.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority" if Config.SERVER_ENV.value == ServerEnv.PRODUCTION.value else
            f"mongodb://localhost:27017/euroapi")
        self.__database = self.__connection.get_database(Config.DB_NAME.value)

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

    def select_one(self, collection: str, ftr: dict, sort_by: [list[tuple], tuple, str, None] = None) -> dict:
        if type(sort_by) is list or type(sort_by) is str:
            return self.__database.get_collection(collection).find_one(ftr).sort(sort_by)
        if type(sort_by) is tuple:
            return self.__database.get_collection(collection).find_one(ftr).sort(sort_by[0], sort_by[1])
        return self.__database.get_collection(collection).find_one(ftr)

    def select_many(self, collection: str, ftr: dict) -> [dict]:
        return self.__database.get_collection(collection).find(ftr)

    def create_collection(self, collection: str):
        self.__database.create_collection(collection)

    def run_command(self, command: dict):
        self.__database.command(command)

    def find_and_update(self, collection: str, condition: dict, data: dict):
        self.__database.get_collection(collection).find_one_and_update(condition, data)

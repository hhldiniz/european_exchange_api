import inspect

from pymongo import MongoClient

from logger import Logger
from util.providers.database_provider import get_provider
from util.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.__database: MongoClient = get_provider().get_database()

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

    def select_one(self, collection: str, ftr: dict, sort_by: [list[tuple], tuple, str, None] = None) -> [dict, None]:
        if type(sort_by) is list or type(sort_by) is str:
            result = self.__database.get_collection(collection).find_one(ftr)
            if result is not None:
                return result.sort(sort_by)
            return result
        if type(sort_by) is tuple:
            result = self.__database.get_collection(collection).find_one(ftr)
            if result is not None:
                return result.sort(sort_by[0], sort_by[1])
            return result
        return self.__database.get_collection(collection).find_one(ftr)

    def select_many(self, collection: str, ftr: dict) -> [dict]:
        Logger.i(f"DatabaseConnection#select_many -> select_many from {collection} collection")
        return self.__database.get_collection(collection).find(ftr)

    def create_collection(self, collection: str):
        Logger.i(f"DatabaseConnection#create_collection -> Creating collection with name {collection}")
        self.__database.create_collection(collection)

    def run_command(self, command: dict):
        all_stack_frames = inspect.stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        Logger.i(f"DatabaseConnection#run_command -> Running command passed by {caller_name}")
        self.__database.command(command)

    def find_and_update(self, collection: str, condition: dict, data: dict):
        Logger.i(f"DatabaseConnection#find_and_update -> Finding and updating collection {collection}")
        self.__database.get_collection(collection).find_one_and_update(condition, data)

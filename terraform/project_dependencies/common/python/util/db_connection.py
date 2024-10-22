import inspect

from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult

from python.logger import Logger
from python.util.providers.database_provider import get_provider
from python.util.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.__database: MongoClient = get_provider().get_database()

    def insert(self, collection: str, data: dict) -> InsertOneResult:
        Logger.i(f"DatabaseConnection#insert -> Inserting on object in collection {collection}")
        print(f"data = {data}")
        return self.__database.get_collection(collection).insert_one(data)

    def insert_many(self, collection: str, data: [dict]) -> InsertManyResult:
        Logger.i(f"DatabaseConnection#insert_many -> "
                 f"Inserting multiple objects in collection {collection}")
        print(f"data = {data}")
        return self.__database.get_collection(collection).insert_many(data)

    def update_one(self, collection: str, condition: dict, data: dict) -> UpdateResult:
        Logger.i(f"DatabaseConnection#update_one -> "
                 f"Updating one object in collection {collection} with condition {condition}")
        print(f"data = {data}")
        return self.__database.get_collection(collection).replace_one(condition, data)

    def update_many(self, collection: str, condition: dict, data: dict) -> UpdateResult:
        Logger.i(f"DatabaseConnection#update_many -> Updating many objects in collection "
                 f"{collection} with condition {condition}")
        print(f"data = {data}")
        return self.__database.get_collection(collection).update_many(condition, data)

    def delete_one(self, collection: str, ftr: dict) -> DeleteResult:
        Logger.i(f"DatabaseConnection#delete_one -> Deleting one object from collection {collection}")
        print(f"ftr = {ftr}")
        return self.__database.get_collection(collection).delete_one(ftr)

    def delete_many(self, collection: str, ftr: dict) -> DeleteResult:
        Logger.i(f"DatabaseConnection#delete_many -> Deleting many objects from collection {collection}")
        print(f"ftr = {ftr}")
        return self.__database.get_collection(collection).delete_many(ftr)

    def select_one(self, collection: str, ftr: dict, sort_by: [list[tuple], tuple, str, None] = None) -> [dict, None]:
        Logger.i(f"DatabaseConnection#select_one -> Finding a single object with params: "
                 f"collection = {collection}, sort_by = {sort_by}")
        print(f"filter = {ftr}")
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
        Logger.i(f"DatabaseConnection#select_many -> select_many from {collection} collection with filter {ftr}")
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

import abc
from abc import ABC
from collections import OrderedDict

from pymongo.errors import CollectionInvalid, BulkWriteError

from python.exceptions.schema_validation_exception import SchemaValidationException
from python.logger import Logger
from python.model.base_model import BaseModel
from python.util.db_connection import DatabaseConnection


class BaseDao(ABC):
    def __init__(self):
        self.db_connection = DatabaseConnection()

    @abc.abstractmethod
    def insert(self, *model: BaseModel):
        self._validate()

    @abc.abstractmethod
    def delete(self, *model: BaseModel):
        self._validate()

    @abc.abstractmethod
    def update(self, *model: BaseModel):
        self._validate()

    @abc.abstractmethod
    def select_one(self, ftr: dict) -> BaseModel:
        pass

    @abc.abstractmethod
    def select_many(self, ftr: dict) -> [BaseModel]:
        pass

    @abc.abstractmethod
    def schema(self) -> dict:
        pass

    @abc.abstractmethod
    def collection(self) -> str:
        pass

    def _validate(self):
        Logger.i("BaseDao#_validate -> Starting schema validation")
        validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
        required = []
        user_schema = self.schema
        collection = self.collection

        l_schema = user_schema if type(user_schema) is dict else user_schema()

        for field_key in l_schema:
            field = l_schema[field_key]
            properties = {'bsonType': field['type']}
            minimum = field.get('minlength')

            if type(minimum) == int:
                properties['minimum'] = minimum

            if field.get('required') is True:
                required.append(field_key)

            validator['$jsonSchema']['properties'][field_key] = properties

        if len(required) > 0:
            validator['$jsonSchema']['required'] = required

        query = [('collMod', collection),
                 ('validator', validator)]

        l_collection = collection if type(collection) is str else collection()
        try:
            self.db_connection.create_collection(l_collection)
            self.db_connection.run_command(OrderedDict(query))
        except CollectionInvalid as e:
            Logger.i(f"BaseDao#_validate: {e}")
        except BulkWriteError:
            raise SchemaValidationException

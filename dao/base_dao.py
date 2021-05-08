import abc
from abc import ABC
from collections import OrderedDict

from pymongo.errors import CollectionInvalid

from exceptions.schema_validation_exception import SchemaValidationException
from model.base_model import BaseModel
from util.db_connection import DatabaseConnection


class BaseDao(ABC):
    def __init__(self):
        self._db_connection = DatabaseConnection()

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
    def schema(self) -> dict:
        pass

    @abc.abstractmethod
    def collection(self) -> str:
        pass

    def _validate(self):
        validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
        required = []
        user_schema = self.schema()
        collection = self.collection()

        for field_key in user_schema:
            field = user_schema[field_key]
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

        try:
            self._db_connection.create_collection(collection)
            self._db_connection.run_command(OrderedDict(query))
        except CollectionInvalid:
            raise SchemaValidationException

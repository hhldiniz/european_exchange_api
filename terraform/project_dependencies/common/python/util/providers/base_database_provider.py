import abc

from pymongo import MongoClient

from terraform.project_dependencies.common.python.config import Config


class BaseDatabaseProvider(abc.ABC):

    @abc.abstractmethod
    def get_connection(self) -> MongoClient:
        pass

    def get_database(self):
        return self.get_connection().get_database(Config.DB_NAME.value)

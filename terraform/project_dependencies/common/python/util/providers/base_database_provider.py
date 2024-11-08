import abc

from pymongo import MongoClient

from config import Config


class BaseDatabaseProvider(abc.ABC):

    @abc.abstractmethod
    def get_connection(self) -> MongoClient:
        pass

    def get_database(self):
        print(f"BaseDatabaseProvider#get_database: Reading from {Config.DB_NAME.value}")
        return self.get_connection().get_database(Config.DB_NAME.value)

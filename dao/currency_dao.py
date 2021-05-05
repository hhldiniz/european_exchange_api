from model.currency import Currency
from util.db_connection import DatabaseConnection


class CurrencyDao:
    def __init__(self):
        self.__db_connection = DatabaseConnection()

    def insert(self, *currency: Currency):
        if currency.__len__() == 1:
            self.__db_connection.insert(self.collection(), currency[0].to_dict())
        elif currency.__len__() > 1:
            self.__db_connection.insert_many(self.collection(),
                                             list(map(lambda this_currency: this_currency.to_dict(), currency)))
        else:
            print("CurrencyDao#insert: Nothing to insert")

    def delete(self, *currency: Currency):
        if currency.__len__() == 1:
            self.__db_connection.delete_one(self.collection(), {'currency_cod': currency[0].currency_code})
        elif currency.__len__() > 1:
            self.__db_connection.delete_many(self.collection(), {'currency_cod': ''})

    @staticmethod
    def schema() -> dict:
        return {
            'currency_code': {
                'type': 'string',
                'length': 3,
                'required': True,
                'coerce': str.upper,
                'nullable': False,
                'unique': True
            },
            'value': {
                'type': 'double',
                'required': True,
                'nullable': False,
            },
            'historical_date': {
                'type': 'string',
                'required': True,
                'nullable': False
            },
            'timestamp': {
                'type': 'string',
                'required': True,
                'nullable': False
            },
            'friendly_name': {
                'type': 'string',
                'required': False,
                'nullable': True
            }
        }

    @staticmethod
    def collection() -> str:
        return "currency"

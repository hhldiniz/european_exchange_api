from dao.base_dao import BaseDao
from model.currency import Currency


class CurrencyDao(BaseDao):
    def __init__(self):
        super().__init__()

    def insert(self, *currency: Currency):
        super().insert(*currency)
        if currency.__len__() == 1:
            self.db_connection.insert(self.collection, currency[0].to_dict())
        elif currency.__len__() > 1:
            self.db_connection.insert_many(self.collection,
                                           list(map(lambda this_currency: this_currency.to_dict(), currency)))
        else:
            print("CurrencyDao#insert: Nothing to insert")

    def delete(self, *currency: Currency):
        super().delete(*currency)
        if currency.__len__() == 1:
            self.db_connection.delete_one(self.collection, {'currency_code': currency[0].currency_code})
        elif currency.__len__() > 1:
            self.db_connection.delete_many(self.collection,
                                           {'currency_code': {
                                               "$set": list(map(lambda this_currency: this_currency.currency_code,
                                                                currency))}})
        else:
            print("CurrencyDao#delete: Nothing to delete")

    def update(self, *currency: Currency):
        super().update(*currency)
        if currency.__len__() == 1:
            self.db_connection.update_one(self.collection, {'currency_code': currency[0].currency_code},
                                          currency[0].to_dict())
        elif currency.__len__() > 1:
            for l_currency in currency:
                self.update(l_currency)
        else:
            print("CurrencyDao#update: Nothing to update")

    def select_one(self, ftr: dict) -> Currency:
        return Currency().from_dict(self.db_connection.select_one(self.collection, ftr))

    def select_many(self, ftr: dict) -> [Currency]:
        return list(
            map(lambda obj: Currency(obj["currency_code"], obj["rate"], obj["historical_date"], obj["timestamp"],
                                     obj["friendly_name"]), self.db_connection.select_many(self.collection, ftr)))

    @property
    def schema(self) -> dict:
        return {
            'currency_code': {
                'type': 'string',
                'length': 3,
                'required': True,
                'coerce': str.upper,
                'nullable': False,
                'unique': True
            },
            'rate': {
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
                'type': 'double',
                'required': True,
                'nullable': False
            },
            'friendly_name': {
                'type': 'string',
                'required': False,
                'nullable': True
            }
        }

    @property
    def collection(self) -> str:
        return "currency"

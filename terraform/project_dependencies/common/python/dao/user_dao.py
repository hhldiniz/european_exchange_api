from dao.base_dao import BaseDao
from model.user import User


class UserDao(BaseDao):
    def insert(self, *user: User):
        pass

    def delete(self, *user: User):
        pass

    def update(self, *user: User):
        pass

    def select_one(self, ftr: dict) -> User:
        pass

    def select_many(self, ftr: dict) -> [User]:
        pass

    @property
    def schema(self) -> dict:
        return {
            "username": {
                "required": True,
                "nullable": False
            },
            "password": {
                "required": True,
                "nullable": False
            }
        }

    @property
    def collection(self) -> str:
        return "user"

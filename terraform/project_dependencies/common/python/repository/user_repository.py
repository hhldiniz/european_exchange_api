from common.python.dao.user_dao import UserDao
from common.python.model.user import User


class UserRepository:
    def __init__(self):
        self.user_dao = UserDao()

    def check_user_login(self, username: str, password: str) -> [User, None]:
        return self.user_dao.select_one({'username': username, 'password': password})

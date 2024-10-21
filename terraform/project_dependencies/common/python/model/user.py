from terraform.project_dependencies.common.python.model.base_model import BaseModel


class User(BaseModel):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def from_dict(self, data: dict):
        return User(data["username"], data["password"])

    def to_dict(self) -> dict:
        return {'username': self.username, 'password': self.password}

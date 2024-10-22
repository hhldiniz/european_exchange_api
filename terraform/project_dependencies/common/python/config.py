import os
from enum import Enum


class Config(Enum):
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    SERVER_ENV = os.getenv("ENVIRONMENT")
    PORT = os.getenv("PORT", 8080)

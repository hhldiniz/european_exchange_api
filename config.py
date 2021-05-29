import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    LOCAL = os.getenv("LOCAL"),
    REMOTE = os.getenv("REMOTE")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    SERVER_ENV = os.getenv("ENVIRONMENT")
    PORT = os.getenv("PORT", 8080)

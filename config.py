import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    LOCAL = os.getenv("LOCAL"),
    REMOTE = os.getenv("REMOTE")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_INSTANCE = os.getenv("DB_INSTANCE")

from python.config import Config
from python.util.providers.local_database_provider import LocalDatabaseProvider
from python.util.providers.remote_database_provider import RemoteDatabaseProvider
from python.util.server_env import ServerEnv


def get_provider():
    provider = RemoteDatabaseProvider() if Config.SERVER_ENV.value == ServerEnv.PRODUCTION.value \
        else LocalDatabaseProvider()
    return provider

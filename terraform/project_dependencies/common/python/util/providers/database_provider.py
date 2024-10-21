from common.python.config import Config
from common.python.util.providers.local_database_provider import LocalDatabaseProvider
from common.python.util.providers.remote_database_provider import RemoteDatabaseProvider
from common.python.util.server_env import ServerEnv


def get_provider():
    provider = RemoteDatabaseProvider() if Config.SERVER_ENV.value == ServerEnv.PRODUCTION.value \
        else LocalDatabaseProvider()
    return provider

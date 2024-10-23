from loguru import logger

from util.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        formatter = (
            "[{level.icon}{level:^10}] {time:YYYY-MM-DD hh:mm:ss} {file} - {name}: {message}"
        )
        level = "INFO"
        file_name = "logger.log"
        logger.add(file_name, format=formatter, level=level, rotation="200 MB", colorize=True)

    @staticmethod
    def d(message, *args, **kwargs):
        logger.debug(message, args, kwargs)

    @staticmethod
    def i(message, *args, **kwargs):
        logger.info(message, args, kwargs)

    @staticmethod
    def w(message, *args, **kwargs):
        logger.warning(message, *args, **kwargs)

    @staticmethod
    def c(message, *args, **kwargs):
        logger.critical(message, *args, **kwargs)

    @staticmethod
    def e(message, *args, **kwargs):
        logger.error(message, *args, **kwargs)

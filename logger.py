from loguru import logger 

level = "INFO"
file_name = "logger.log"

formatter = (
    "[{level.icon}{level:^10}] {time:YYYY-MM-DD hh:mm:ss} {file} - {name}: {message}"
)

logger.add(file_name, format=formatter, level=level, rotation="200 MB", colorize=True)

if __name__ == "__main__":
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")

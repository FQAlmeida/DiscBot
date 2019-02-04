import logging


def setup_logger():
    # .log file will be kept in data folder, under logger.log name
    logger = logging.getLogger('data\logger')

    # Log level = DEBUG
    logger.setLevel(logging.DEBUG)

    # Handler for logging events format and save in the file
    handler = logging.FileHandler(filename='data\logger.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    logger.INFO = logging.INFO
    logger.DEBUG = logging.DEBUG
    logger.ERROR = logging.ERROR
    logger.CRITICAL = logging.CRITICAL
    logger.WARNING = logging.WARNING
    logger.NOTSET = logging.NOTSET

    return logger

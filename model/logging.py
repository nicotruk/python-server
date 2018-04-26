import logging

logging_level = logging.DEBUG
# logging_level = logging.INFO
# logging_level = logging.WARNING
# logging_level = logging.ERROR
# logging_level = logging.CRITICAL


def configure_logger():
    logging.basicConfig(filename='python-server.log', level=logging_level)

import logging


def configure_logger():
    logging_level = logging.DEBUG
    # logging_level = logging.INFO
    # logging_level = logging.WARNING
    # logging_level = logging.ERROR
    # logging_level = logging.CRITICAL
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='python-server.log',
                        level=logging_level)

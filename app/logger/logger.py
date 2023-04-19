import sys
from logging import getLogger, INFO, StreamHandler, Formatter, FileHandler

log_format = '%(asctime)s [%(levelname)s][%(pathname)s: %(funcName)s: ' \
             '%(lineno)d]: %(message)s'

stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(Formatter(fmt=log_format))

file_handler = FileHandler(filename='logs.log')
file_handler.setFormatter(Formatter(fmt=log_format))

logger = getLogger(__name__)
logger.setLevel(INFO)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
import logging
import sys

import config

if config.get('loggin.level') == 'DEBUG':
    level = logging.DEBUG
elif config.get('loggin.level') == 'INFO':
    level = logging.INFO
elif config.get('loggin.level') == 'WARNING':
    level = logging.WARNING
elif config.get('loggin.level') == 'ERROR':
    level = logging.ERROR
elif config.get('loggin.level') == 'CRITICAL':
    level = logging.CRITICAL
else:
    level = logging.NOTSET

formatter = logging.Formatter('%(levelname)s - %(message)s')

logging.basicConfig(level=level, formatter=formatter)

logger = logging.getLogger()
logger.handlers = []

streamHandle = logging.StreamHandler(stream=sys.stdout)
streamHandle.setLevel(level)
streamHandle.setFormatter(formatter)
logger.addHandler(streamHandle)

fileHandle = logging.FileHandler("/var/log/" + config.get('loggin.filename'))
fileHandle.setLevel(level)
fileHandle.setFormatter(formatter)
logger.addHandler(fileHandle)

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error
critical = logger.critical

def show():
    with open("/var/log/" + config.get('loggin.filename')) as f:
        print("".join(f.readlines()))

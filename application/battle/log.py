import logging
import sys

import config

if config.get('logging.battle.level') == 'UNITS':
    level = 11
elif config.get('logging.battle.level') == 'GROUP':
    level = 12
elif config.get('logging.battle.level') == 'FRONT':
    level = 13
elif config.get('logging.battle.level') == 'BATTLE':
    level = 14
elif config.get('logging.battle.level') == 'INFO':
    level = logging.INFO
elif config.get('logging.battle.level') == 'WARNING':
    level = logging.WARNING
elif config.get('logging.battle.level') == 'ERROR':
    level = logging.ERROR
elif config.get('logging.battle.level') == 'CRITICAL':
    level = logging.CRITICAL
else:
    level = logging.NOTSET

formatter = logging.Formatter('%(levelname)s - %(message)s')

logging.basicConfig(level=level, formatter=formatter)
logging.addLevelName(11, '      UNITS')
logging.addLevelName(12, '    GROUP')
logging.addLevelName(13, '  FRONT')
logging.addLevelName(14, '\nBATTLE')

logger = logging.getLogger()
logger.handlers = []

if config.get('loggin.stream') == 'True':
    streamHandle = logging.StreamHandler(stream=sys.stdout)
    streamHandle.setLevel(level)
    streamHandle.setFormatter(formatter)
    logger.addHandler(streamHandle)

def initFileLogger(battleId):
    if config.get('loggin.filename') != 'False':
        fileHandle = logging.FileHandler("/var/log/" + config.get('loggin.battle.dir') + '/%s' + battleId)
        fileHandle.setLevel(level)
        fileHandle.setFormatter(formatter)
        logger.addHandler(fileHandle)

def unit(msg, *args, **kwargs):
    logger.log(11, msg, *args, **kwargs)

def group(msg, *args, **kwargs):
    logger.log(12, msg, *args, **kwargs)

def front(msg, *args, **kwargs):
    logger.log(13, msg, *args, **kwargs)

def battle(msg, *args, **kwargs):
    logger.log(14, msg, *args, **kwargs)


info = logger.info
warn = logger.warning
error = logger.error
critical = logger.critical

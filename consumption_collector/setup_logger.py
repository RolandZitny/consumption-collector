import sys
import logging
from config import get_config


_nameToLevel = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}


DEBUGGING_LOG_LEVEL = {
    'client': logging.INFO,
}


def log_level(level) -> int:
    """
        Method convert text representation of log level to int log level.
    """
    if isinstance(level, str):
        _level = level.upper()
        if _level not in _nameToLevel:
            raise AttributeError('Unknown log level "{}"'.format(level))
        return _nameToLevel[_level]
    return level


LOG_LEVEL = get_config('LOGGER_LEVEL', wrapper=log_level)

for log_name, level in DEBUGGING_LOG_LEVEL.items():
    logging.getLogger(log_name).setLevel(level)

root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)


logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


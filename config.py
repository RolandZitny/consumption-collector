"""
Configuration file for Docker.
This file consists from SLMPClient parameters and InfluxDB parameters.
"""
import os
import logging
from typing import Callable

DEFAULT_CONFIG = {
    # slmpclient
    'SLMP_IP_ADDR': '192.168.10.201',
    'SLMP_PORT': 4050,
    'SLMP_TCP': 1,
    # InfluxDB
    'INFLUX_URL': 'URL INFLUXDB',
    'INFLUX_TOKEN': 'token',
    'INFLUX_ORG': 'org',
    'INFLUX_BUCKET': 'bucket',
    # async comm sleep
    'DATA_SLEEP': 0.0010,   # When getting data from robot sleep 1ms
    'FLUSH_SLEEP': 3,        # Flush  every 3 seconds
    'LOGGER_LEVEL': 'INFO'
}


def get_config(name: str, default=None, wrapper: Callable = None):
    if not wrapper:
        wrapper = lambda x: x  # NOQA
    return wrapper(os.getenv(name, DEFAULT_CONFIG.get(name, default)))


_nameToLevel = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
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


logger = logging.getLogger('collector')
logger.setLevel(log_level(get_config('LOGGER_LEVEL')))

"""
Configuration file for Docker.
This file consists from SLMPClient parameters and InfluxDB parameters.
"""
import os
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
    'LOGGER_LEVEL': 'DEBUG'
}


def get_config(name: str, default=None, wrapper: Callable = None):
    if not wrapper:
        wrapper = lambda x: x  # NOQA
    return wrapper(os.getenv(name, DEFAULT_CONFIG.get(name, default)))

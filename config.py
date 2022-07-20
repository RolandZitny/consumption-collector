"""
Configuration file for Docker.
This file consists from SLMPClient parameters and InfluxDB parameters.
"""
import os
from typing import Callable

DEFAULT_CONFIG = {
    # slmpclient
    'SLMP_IP_ADDR': '10.54.2.76',
    'SLMP_PORT': 4070,
    'SLMP_TCP': True,
    # InfluxDB
    'INFLUX_URL': '10.54.2.76:4050',
    'INFLUX_TOKEN': 'token',
    'INFLUX_ORG': 'org',
    'INFLUX_BUCKET': 'bucket'
}


def get_config(name: str, default=None, wrapper: Callable = None):
    if not wrapper:
        wrapper = lambda x: x  # NOQA
    return wrapper(os.getenv(name, DEFAULT_CONFIG.get(name, default)))

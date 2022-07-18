"""
Configuration file for Docker.
This file consists from SLMPClient parameters and InfluxDB parameters.
"""
import os
from typing import Callable

DEFAULT_CONFIG = {
    # slmpclient
    'SLMP_IP_ADDR': '127.0.0.1',
    'SLMP_PORT': 4067,
    'SLMP_TCP': True,
    # InfluxDB
    'INFLUX_URL': 'http://localhost:4050',
    'INFLUX_TOKEN': 'qKbKhyK47-oxSOwJwiv_sUdqAVM1Uq9q2e64AC42Yf6_k8V1M-gs0iQKGFmAQtsjtgJQkcPM8TmDs6hG9nLTYQ==',
    'INFLUX_ORG': 'ALPSRobot',
    'INFLUX_BUCKET': 'slmp'
}


def get_config(name: str, default=None, wrapper: Callable = None):
    if not wrapper:
        wrapper = lambda x: x  # NOQA
    return wrapper(os.getenv(name, DEFAULT_CONFIG.get(name, default)))

import asyncio
import time

from influxdb_client.client.influxdb_client import InfluxDBClient


class Collector:
    def __init__(self, communicator=None, url=None, token=None, org=None, bucket=None):
        self._communicator = communicator
        self._url = url
        self._token = token
        self._org = org
        self._bucket = bucket

    def push_data(self, points_queue):
        with InfluxDBClient(url=self._url, token=self._token, org=self._org) as influxclient:
            write_api = influxclient.write_api()
            record = []

            while len(points_queue) != 0:
                record.append(points_queue.pop(0))

            successfully = write_api.write(bucket=self._bucket, record=record)
            print(f" > successfully: {successfully}")


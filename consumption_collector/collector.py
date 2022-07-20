"""
Collector collects data from some type of communicator, which produces this data in the form of influx points.
These data are stored in a queue and after a defined time are flushed to the database (InfluxDB).
"""
from influxdb_client.client.influxdb_client import InfluxDBClient


class Collector:
    def __init__(self, url=None, token=None, org=None, bucket=None):
        """
        Initialize Collector class and set parameters for InfluxDBClient.
        :param url: InfluxDB url
        :param token: InfluxDB token
        :param org: InfluxDB organization
        :param bucket: InfluxDB bucket
        """
        print("COLLECTOR INIT")
        self._url = url
        self._token = token
        self._org = org
        self._bucket = bucket
        self._points_queue = []                  # Queue for points

    def save_point(self, point):
        """
        Method for saving/uploading points into Collectors queue.
        :param point: InfluxDB point
        """
        self._points_queue.append(point)

    def flush_data(self):
        """
        Method for flushing data into InfluxDB. This method needs to be called at defined intervals.
        This method takes all data from Collectors points_queue, till it reach empty queue.
        """
        with InfluxDBClient(url=self._url, token=self._token, org=self._org) as influx_client:
            write_api = influx_client.write_api()
            record = []
            print("self._points_queue:   ", len(self._points_queue))
            while len(self._points_queue) != 1:
                record.append(self._points_queue.pop(0))

            print("record DB:   ", len(record))
            write_api.write(bucket=self._bucket, record=record)


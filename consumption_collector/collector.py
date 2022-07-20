"""
Collector collects data from some type of communicator, which produces this data in the form of influx points.
These data are stored in a queue and after a defined time are flushed to the database (InfluxDB).
"""
from datetime import datetime
from influxdb_client import Point, WriteOptions, WritePrecision
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
        # TODO batch in
        with InfluxDBClient(url=self._url, token=self._token, org=self._org) as _client:
            with _client.write_api(write_options=WriteOptions(batch_size=1000,
                                                              flush_interval=4_000,
                                                              jitter_interval=0,
                                                              retry_interval=5_000,
                                                              max_retries=5,
                                                              max_retry_delay=30_000,
                                                              exponential_base=2)) as _write_client:
                data = [0,1,2,3,4,5]
                point = (Point("slmp").tag('Robotic Arm', 'ID')
                         .field("M32", int(data[0]))
                         .field("M33", int(data[1]))
                         .field("M34", int(data[2]))
                         .field("M35", int(data[3]))
                         .field("M36", int(data[4]))
                         .field("M37", int(data[5]))
                         .time(datetime.utcnow(), WritePrecision.MS))
                _write_client.write(bucket=self._bucket, org=self._org, point=point)
        """
        with InfluxDBClient(url=self._url, token=self._token, org=self._org) as influx_client:
            write_api = influx_client.write_api()
            record = []
            print("self._points_queue:   ", len(self._points_queue))
            while len(self._points_queue) != 1:
                record.append(self._points_queue.pop(0))

            print("record DB:   ", len(record))
            write_api.write(bucket=self._bucket, record=record)
        """

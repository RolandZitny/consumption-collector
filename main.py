"""
Main program of asynchronous communication between Mitsubishi robotic arm and InfluxDB for collecting time series data.
"""
from influxdb_client import WriteOptions
from influxdb_client.client.influxdb_client import InfluxDBClient

import asyncio
from config import get_config
from consumption_collector.communicator import Communicator
from consumption_collector.collector import Collector


async def obtain_point(com, sleep_time):
    """
    Asynchronous function for reading energy consumption from 6 register of robotic arm.
    :param sleep_time: interval of reading in seconds
    :param com: Communicator class
    """
    while True:
        await asyncio.sleep(sleep_time)
        com.send_request()
        com.get_point()


async def collect_points(coll, sleep_time):
    """
    Asynchronous function for flushing obtained data from robotic arm into InfluxDB.
    :param sleep_time:
    :param coll: Collector class
    """
    while True:
        await asyncio.sleep(sleep_time)
        coll.flush_data()


if __name__ == "__main__":
    """
    collector = Collector(url=get_config('INFLUX_URL'),
                          token=get_config('INFLUX_TOKEN'),
                          org=get_config('INFLUX_ORG'),
                          bucket=get_config('INFLUX_BUCKET'))

    communicator = Communicator(ipaddr=get_config('SLMP_IP_ADDR'),
                                port=get_config('SLMP_PORT', wrapper=int),
                                tcp=get_config('SLMP_TCP', wrapper=int),
                                collector=collector)

    loop = asyncio.get_event_loop()
    loop.create_task(obtain_point(communicator, get_config('DATA_SLEEP', wrapper=float)))
    loop.create_task(collect_points(collector, get_config('FLUSH_SLEEP', wrapper=float)))
    loop.run_forever()
    """
    communicator = Communicator(ipaddr=get_config('SLMP_IP_ADDR'),
                                port=get_config('SLMP_PORT', wrapper=int),
                                tcp=get_config('SLMP_TCP', wrapper=int),
                                collector=None)
    with InfluxDBClient(url=get_config('INFLUX_URL'),
                        token=get_config('INFLUX_TOKEN'),
                        org=get_config('INFLUX_ORG')) as _client:
        with _client.write_api(write_options=WriteOptions(batch_size=500,
                                                          flush_interval=3_000,
                                                          jitter_interval=0,
                                                          retry_interval=5_000,
                                                          max_retries=5,
                                                          max_retry_delay=30_000,
                                                          exponential_base=2)) as write_client:
            while True:
                communicator.send_request()
                communicator.get_point(write_client)


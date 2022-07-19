"""
Main program of asynchronous communication between Mitsubishi robotic arm and InfluxDB for collecting time series data.
"""
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
    collector = Collector(url=get_config('INFLUX_URL'),
                          token=get_config('INFLUX_TOKEN'),
                          org=get_config('INFLUX_ORG'),
                          bucket=get_config('INFLUX_BUCKET'))

    communicator = Communicator(ipaddr=get_config('SLMP_IP_ADDR'),
                                port=get_config('SLMP_PORT', wrapper=int),
                                tcp=True,
                                collector=collector)

    loop = asyncio.get_event_loop()
    loop.create_task(obtain_point(communicator, 3.5/1000))
    loop.create_task(collect_points(collector, 3))
    loop.run_forever()


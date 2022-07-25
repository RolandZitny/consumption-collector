"""
Main program of asynchronous communication between Mitsubishi robotic arm and InfluxDB for collecting time series data.
"""
from asyncio import sleep, get_event_loop
from config import get_config
from setup_logging import logger
from consumption_collector.collector import Collector
from consumption_collector.communicator import Communicator


async def obtain_point(com, sleep_time):
    """
    Asynchronous function for reading energy consumption from 6 register of robotic arm.
    :param sleep_time: read interval in seconds
    :param com: Communicator class
    """
    while True:
        await sleep(sleep_time)
        com.get_point()


async def collect_points(coll, sleep_time):
    """
    Asynchronous function for flushing obtained data from robotic arm into InfluxDB.
    :param sleep_time: flush interval in seconds
    :param coll: Collector class
    """
    while True:
        await sleep(sleep_time)
        coll.flush_data()
        logger.debug('Flush data')


def main():
    """
    Start two asynchronous parallel cycles.
    One cycle is for obtaining data points from robotic arm.
    Second cycle is for flushing obtained data into InfluxDB.
    """
    logger.info('Start main program.')
    collector = Collector(url=get_config('INFLUX_URL'),
                          token=get_config('INFLUX_TOKEN'),
                          org=get_config('INFLUX_ORG'),
                          bucket=get_config('INFLUX_BUCKET'))

    communicator = Communicator(ipaddr=get_config('SLMP_IP_ADDR'),
                                port=get_config('SLMP_PORT', wrapper=int),
                                tcp=get_config('SLMP_TCP', wrapper=int),
                                collector=collector)

    loop = get_event_loop()
    loop.create_task(obtain_point(communicator, get_config('DATA_SLEEP', wrapper=float)))
    loop.create_task(collect_points(collector, get_config('FLUSH_SLEEP', wrapper=float)))
    loop.run_forever()


if __name__ == "__main__":
    main()


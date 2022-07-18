"""
Main program of asynchronous communication between Mitsubishi robotic arm and InfluxDB for collecting time series data.
"""
import asyncio
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
        print("Send")

if __name__ == "__main__":
    collector = Collector(url="http://localhost:4050",
                          token="qKbKhyK47-oxSOwJwiv_sUdqAVM1Uq9q2e64AC42Yf6_k8V1M-gs0iQKGFmAQtsjtgJQkcPM8TmDs6hG9nLTYQ==",
                          org="ALPSRobot",
                          bucket="slmp")
    communicator = Communicator(ipaddr="127.0.0.1", port=4067, tcp=True, collector=collector)

    loop = asyncio.get_event_loop()
    loop.create_task(obtain_point(communicator, 1))
    loop.create_task(collect_points(collector, 3))
    loop.run_forever()


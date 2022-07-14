import asyncio
from consumption_collector.communicator import Communicator
from consumption_collector.collector import Collector


async def a(com, queue):
    while True:
        await asyncio.sleep(6)
        com.send_request()
        com.get_point(queue)


async def b(coll, queue):
    while True:
        await asyncio.sleep(15)
        coll.push_data(queue)


if __name__ == "__main__":
    points_queue = []
    communicator = Communicator(ipaddr="127.0.0.1", port=4067, tcp=True)
    collector = Collector(communicator=communicator,
                          url="http://localhost:4050",
                          token="eFwD0aYM1y_Bso5QOattValItAeTjDfdnutb1F_ROdfJSKbn6Lij4BsxWu7Au5Od_RhP9_03V6TPjXL6SrsK9w== ",
                          org="ALPSRobot",
                          bucket="slmp")

    loop = asyncio.get_event_loop()
    loop.create_task(a(communicator, points_queue))
    loop.create_task(b(collector, points_queue))
    loop.run_forever()


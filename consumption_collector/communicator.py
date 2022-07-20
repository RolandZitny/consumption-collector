"""
Communicator communicate with Mitsubishi robotic arm, using SLMP protocol and slmpclient
library from https://pypi.org/project/slmpclient/. Check documentation there to understand creation of messages.
This communicator serves to obtain values of energy consumption registers, which are 6 of them and 1 register is
synchronization flag.
Response is parsed and from data are created InfluxDB points, which are saved into internal queue of Collector.
"""
import time
import struct
from datetime import datetime
from influxdb_client import Point, WritePrecision
from slmpclient import SLMPClient, SLMPPacket, FrameType, ProcessorNumber, TimerValue, SLMPCommand, SLMPSubCommand


class Communicator:
    def __init__(self, ipaddr=None, port=None, tcp=True, collector=None):
        """
        Initialize Communicator.
        Communicator
        :param ipaddr: IP ADDR of robotic arm
        :param port: PORT or robotic arm
        :param tcp: Flag -> True = TCP, False = UDP
        :param collector: Collector class, where to save points.
        """
        self._collector = collector
        self._client = SLMPClient(ip_addr=ipaddr, port=port, protocol=tcp)
        self._client.open()

        pucData = b'\xAC\x12\x00\xA8\x1C\x00'  # Reading will start from register D4780, and takes 28 words
        slmp_controller = SLMPPacket(ulFrameType=FrameType.SLMP_FTYPE_BIN_REQ_ST.value,
                                     usNetNumber=0,
                                     usNodeNumber=0xFF,
                                     usProcNumber=ProcessorNumber.SLMP_CPU_DEFAULT.value,
                                     usTimer=TimerValue.SLMP_TIMER_WAIT_FOREVER.value,
                                     usCommand=SLMPCommand.SLMP_COMMAND_DEVICE_READ.value,
                                     usSubCommand=SLMPSubCommand.SUB_word0.value, pucData=pucData)

        self._request = slmp_controller.create_stream()
        self._TAKE_FLAG = True
        self._response = None

    def parse_response(self, response, print_flag=False):
        """
        Parsing of SLMP response.
        :param response: response
        :param print_flag: DEBUG flag to print response
        """
        end_code = response[8:10]
        if end_code != b'\x00\x00' or len(response) < 67:
            print("parse ERR")  # TODO log
            exit(1)

        response_data_part = response[11:67]
        data = struct.unpack('<ddddddd', response_data_part)

        # Synchronization to not take data again if they are the same.
        if data[0] == 1 and self._TAKE_FLAG is True:
            flag = True
            self._TAKE_FLAG = False
        else:
            flag = False
            self._TAKE_FLAG = True

        # Just print out data
        if print_flag is True:
            print("M38          : ", data[0])
            print("M37          : ", data[1])
            print("M36          : ", data[2])
            print("M35          : ", data[3])
            print("M34          : ", data[4])
            print("M33          : ", data[5])
            print("M32          : ", data[6])
            print("")

        return flag, [data[6], data[5], data[4], data[3], data[2], data[1]]

    def send_request(self):
        """
        Send request to robotic arm.
        """
        self._client.send(self._request)
        self._response = self._client.receive()

    def get_point(self):
        """
        Creates Influx point from response and save into internal queue of Collector.
        """
        #ready_flag, data = self.parse_response(self._response)
        ready_flag = True
        data = [0, 1, 2, 3, 4, 5]
        if ready_flag:
            point = (Point("slmp").tag('Robotic Arm', 'XXX')
                     .field("M32", int(data[0]))
                     .field("M33", int(data[1]))
                     .field("M34", int(data[2]))
                     .field("M35", int(data[3]))
                     .field("M36", int(data[4]))
                     .field("M37", int(data[5]))
                     .time(datetime.utcnow(), WritePrecision.MS))
            self._collector.save_point(point)   # Save into Collector
            print("save_point")





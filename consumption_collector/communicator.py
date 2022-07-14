import struct
import time
from datetime import datetime
from slmpclient import SLMPClient, SLMPPacket, FrameType, ProcessorNumber, TimerValue, SLMPCommand, SLMPSubCommand
from influxdb_client import Point


class Communicator:
    def __init__(self, ipaddr=None, port=None, tcp=True):
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
        end_code = response[8:10]
        if end_code != b'\x00\x00' or len(response) < 67:
            print("parse ERR")  # TODO log
            exit(1)

        response_data_part = response[11:67]
        data = struct.unpack('<ddddddd', response_data_part)

        # Take flag TODO naming
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
        self._client.send(self._request)
        self._response = self._client.receive()

    def get_point(self, points_queue):
        ready_flag, data = self.parse_response(self._response)
        if ready_flag:
            point = (Point("slmp").tag("timestamp", time.time())
                     .field("M32", int(data[0]))
                     .field("M33", int(data[1]))
                     .field("M34", int(data[2]))
                     .field("M35", int(data[3]))
                     .field("M36", int(data[4]))
                     .field("M37", int(data[5])))
            points_queue.append(point)





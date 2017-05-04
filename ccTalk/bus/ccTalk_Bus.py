import serial.tools.list_ports as list
import serial
from ccTalk.bus.ccTalk_Message import ccTalk_Message
'''
This class will handle the complete communication. 
The method are tryied to be named like in my c++  implementation

@author: kri


'''

class ccTalk_Bus:
    #List of all used ports
    _cctalk_open_ports__ = {}
    port = serial.Serial()
    _is_initialized = False

    def __init__(self,portname:str):
        self.portname = portname

    def __str__(self):
        return self.portname+" "+str(self.open)

    #We try to be sure we only have each port used once
    @classmethod
    def by_port_name(cls, portname: str):
        if portname in cls._cctalk_open_ports__:
            return cls._cctalk_open_ports__[portname]
        else:
            bus = ccTalk_Bus(portname)
            cls._cctalk_open_ports__[portname] = bus
            return bus

    #Initialize the bus.
    def initialize(self, baudrate:int=9600):
        self.port.baudrate = baudrate
        #This need to be done to be Jankowski compatible... STFU
        self.port.setDTR(False)
        self.port.port = self.portname
        self._is_initialized = True
        return self._is_initialized

    #open the port for communication
    def open(self):
        self.port.open()
        return self.is_open

    #close the port
    def close(self):
        self.port.close()
        return True

    #We want to send a ccTalk_Message where only ack is expected
    def send_cctalk_simple_message(self, message:ccTalk_Message):
        #We send the bytes. Our serial is working in bytes!
        if self.send_message_bytes(bytes(message)):
            return ccTalk_Message.verify_answer_bytes(self.read_bytes()) #We expect a correct ack


    #We want to send a ccTalk_Message where we need an answer
    def send_cctalk_request_message(self, message:ccTalk_Message):
        #We send the bytes. Our serial is working in bytes!
        if self.send_message_bytes(bytes(message)):
            answer = self.read_bytes()
            if ccTalk_Message.verify_from_bytes(answer):
                return ccTalk_Message.from_bytes(answer)
            return False

    #We want to send a ccTalk_Message where only ack is expected
    def send_bytes_simple_message(self, message:bytes):
        #make sure we have a checksum
        if len(message) < message[1]+5:
            message+=bytes([ccTalk_Message.make_simple_checksum_for_bytes(message)])
        #We send the bytes. Our serial is working in bytes!
        if self.send_message_bytes(message):
            return ccTalk_Message.verify_answer_bytes(self.read_bytes()) #We expect a correct ack
        return False

    #We want to send a ccTalk_Message where we need an answer
    def send_bytes_request_message(self, message:bytes):
        #make sure we have a checksum
        if len(message) < message[1]+5:
            message+=bytes([ccTalk_Message.make_simple_checksum_for_bytes(message)])
        #We send the bytes. Our serial is working in bytes!
        if self.send_message_bytes(bytes(message)):
            answer = self.read_bytes()
            if ccTalk_Message.verify_from_bytes(answer):
                return answer
            return False

    #Send the byte array to the line
    def send_message_bytes(self, message: bytes):
        self.port.write(message)
        return self.read_echo(message)

    #Check is the echo is what we expected!
    def read_echo(self, expect:bytes):
        if (self.port.read(len(expect))==expect):
            return True
        return False

    #read some bytes. This can be used for known and unknown length!
    def read_bytes(self, len:int=0):
        if len !=0:
            return self.port.read(len)
        #read 2 bytes. second is the expected number
        first = self.port.read(2)
        second = self.port.read(int(first[1])+3)
        answer = bytes(first+second)
        return answer


    #Following simple getter and setter
    @property
    def is_initialized(self):
        return self._is_initialized

    @property
    def is_open(self):
        return self.port.is_open

    @staticmethod
    def list_available_ports():
        ports = ""
        for port in list.comports():
            ports = ports+str(port)+'\n'
        return ports
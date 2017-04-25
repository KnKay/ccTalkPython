import serial.tools.list_ports as list
import serial
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
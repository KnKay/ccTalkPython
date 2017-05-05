'''
Scope of this snippit is to test polling.
This is done during normal operation.

We will first read the unit information. After this we 
get the coins, extract the values and will make some coin handling.
'''

from ccTalk.bus.ccTalk_Bus import ccTalk_Bus
from ccTalk.bus.ccTalk_Message import ccTalk_Message
from ccTalk.helper.event_hander import *
import threading

import os
import time
port = "COM4"

coin_values = []


#Init the bus
'''
print("This is a simple demo")
print(ccTalk_Bus.list_available_ports())
port = input("Please enter name of port to be used: \n").upper()
rcp_file_root = os.path.expanduser("~")+os.sep+"Documents"+os.sep+"rcpdist"+os.sep+"files"+os.sep
print (rcp_file_root)
print(port, " will be used")
'''
validator_address = 2
bus = ccTalk_Bus(port)
bus.initialize()
bus.open()

#Read relevant information out of the coin Validator. This is used to determine the correct files.
validator = ccTalk_Message.get_payload_from_bytes(bus.send_bytes_request_message(bytes([validator_address, 0, 1, 244]))).decode("UTF-8")
print("Connected :",validator)

failure = False

#we reset the unit. Otherwise the event counter will be where ever it has been before we start!
if not bus.send_bytes_simple_message(bytes([validator_address,0,1,1])):
    print ("Reset with error")
time.sleep(1)
#To accept the unit we want to disable master inhibit and set the single inhibits to 0
if not bus.send_bytes_simple_message(bytes([validator_address,2,1,231,0xff,0xff])):
    print ("Failure during inhibit")
    failure = True
if not bus.send_bytes_simple_message(bytes([validator_address,1,1,228,0x01])):
    print ("Failure master inhibit")
    failure = True


poll_command = bytes([validator_address, 0, 1, 229])
#The event buffer is only 0 after reset
bus.send_bytes_request_message(bytes([validator_address, 0, 1, 229]))
handled_events = 1

#poll_loop(handled_events,poll_command,bus)
stop_event = threading.Event()
thread1 = poll_thread(stop_event, bus, validator_address, poll_command)
thread1.start()
input("Press any key to quit")
stop_event.set()
bus.close()
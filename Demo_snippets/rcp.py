#We import classes for the ccTalk bus and ccTalk Message.
from ccTalk.bus.ccTalk_Bus import ccTalk_Bus
from ccTalk.bus.ccTalk_Message import ccTalk_Message

from ccTalk.helper.rcp import *

#Used for file walking and finding files
from pathlib import Path
import os
import time

#The following is needed to determin what should be programmed.
port= "COM4" # Nail this down for test!

#open the bus and initialize it.
#print("This is a simple demo")
#print(ccTalk_Bus.list_available_ports())
#port = input("Please enter name of port to be used: \n").upper()
validator_address = 2
rcp_file_root = os.path.expanduser("~")+os.sep+"Documents"+os.sep+"rcpdist"+os.sep+"files"+os.sep
print (rcp_file_root)
print(port, " will be used")
bus = ccTalk_Bus(port)
bus.initialize()
bus.open()

#Read relevant information out of the coin Validator. This is used to determine the correct files.
validator = ccTalk_Message.get_payload_from_bytes(bus.send_bytes_request_message(bytes([validator_address, 0, 1, 244]))).decode("UTF-8")
database_version = ccTalk_Message.get_payload_from_bytes(bus.send_bytes_request_message(bytes([validator_address, 0, 1, 243])))
database_version = "Db-00"+str(int.from_bytes(database_version, byteorder='little')) # This is needed int python
build_code = ccTalk_Message.get_payload_from_bytes(bus.send_bytes_request_message(bytes([validator_address, 0, 1, 192]))).decode("UTF-8")
if validator == "SR5i":
    validator = "eagle"
print("Connected :",validator,build_code,database_version)

#go to the corresponding folder
rcp_file_root = Path(rcp_file_root+os.sep+validator+os.sep+"DE0"+os.sep+"Bin"+os.sep+database_version)
#Check if the relevant data have a structure from a given root. The structure is aligned to the ccTalk Specification
#If the path is valid we set our files root to this.
'''
print ("Available Consets:")
for folder in [folder for folder in  rcp_file_root.glob('*') if folder.is_dir()]:
    print (str(folder).split(os.sep)[-1]) # Get only the Folder Name. This is our coinset
'''

#Ask for the Coinset, go into set and list coins. Ask the customer for the used channel

coinset = "EU" #coinset = input("Please enter name of coinset to be used: \n")
file_folder = Path(str(rcp_file_root)+os.sep+coinset)
print ("Available Coins:")
for file in [file for file in  file_folder.glob('*') if file.is_file()]:
    print (str(file).split(os.sep)[-1]) # Get only the Folder Name. This is our coinset
coin =  "EU010A-0.bin" #coin = input("Please enter name of coin to be used: \n")
coinfile = str(file_folder)+os.sep+coin


#Finally print an overview of what is now in the validator

print ("Channels in the unit: ")
for channel in range(1,17):
    print (channel,"\t", ccTalk_Message.get_payload_from_bytes(bus.send_bytes_request_message(bytes([validator_address, 1, 1, 184, channel]))).decode("UTF-8"))

channel = 10 #input("Please enter name of channel to be used: \n")
channel = int(channel)
if program_rcp_file(bus,coinfile,validator_address,channel)== True:
    print ("Programmed channel",channel)
    print(channel, "\t", ccTalk_Message.get_payload_from_bytes(
        bus.send_bytes_request_message(bytes([validator_address, 1, 1, 184, channel]))).decode("UTF-8"))
rcp_erase_coin_channel(bus,validator_address,channel)
bus.close()
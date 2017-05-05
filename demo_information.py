from ccTalk.bus.ccTalk_Bus import ccTalk_Bus, ccTalk_Message
import serial.tools.list_ports as list

'''
Make a simple demo.
We wil lread out the name of the unit etc. 

'''
if __name__ == "__main__":
    print("This is a simple demo")
    print (ccTalk_Bus.list_available_ports())
    port = input("Please enter name of port to be used: \n").upper()
    print (port, " will be used")
    bus = ccTalk_Bus(port)
    bus.close()
    bus.initialize()
    bus.open()
    if(bus.is_open):
        print ("Connected Device:")
        print (ccTalk_Message.get_payload_from_bytes(bus.send_bytes_request_message(bytes([2, 0, 1, 244])))) #We get an answer from bytes in bytes
        print (bus.send_cctalk_request_message(ccTalk_Message.from_bytes([2, 0, 1, 245])).payload) #We get a ccTalk answer if request is ccTalk
        print(bus.send_cctalk_request_message(ccTalk_Message.from_bytes([2, 0, 1, 246])).payload)





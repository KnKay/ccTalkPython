from ccTalk.bus.ccTalk_Bus import ccTalk_Bus
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
    print(ccTalk_Bus.by_port_name("port"))
    print(ccTalk_Bus.by_port_name("port"))


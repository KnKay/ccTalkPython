from ccTalk.bus.ccTalk_Bus import ccTalk_Bus
#This is programming the file into our validator


def program_rcp_file(bus:ccTalk_Bus,file:str, channel:int):
    print ("Programming",file,"to channel",channel)
    '''
    Open the file. If this is not working we need to break
    
    '''
    file = open(file, 'r')
    if not file:
        print ("Cannot open file")
        return False
    '''
    Set the validator into programming mode. -> if no ack no action
    Message to reach programming mode is:
        Destination adddress                (2 for a normal validator)
        Payload Size/Number of data bytes   (1, as we use a sub header
        Source  address                     (1, as we are the master)
        Header                              (Must be 96)
        Payload (Subheader)                 (Must be 255)
    '''
    print (bus.send_bytes_simple_message(bytes([2, 1, 1, 96, 255])))

    return False

    if not bus.send_bytes_simple_message(bytes([2,1,1,96,255])):
        #We need some better Failure Handling
        print("Error during enter programming mode")
        return False

    return True

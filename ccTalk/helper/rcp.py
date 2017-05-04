from ccTalk.bus.ccTalk_Bus import ccTalk_Bus, ccTalk_Message
import os, time
#This is programming the file into our validator

#We need to know which bus, which file, the address of the validator, the destination channel an package size
def program_rcp_file(bus:ccTalk_Bus, file:str, dest:int, channel:int, package_size:int=255):
    print ("Programming",file,"to channel",channel)
    '''
    Set the validator into programming mode. -> if no ack no action
    Message to reach programming mode is:
        Destination adddress                
        Payload Size/Number of data bytes   (1, as we use a sub header
        Source  address                     (1, as we are the master)
        Header                              (Must be 96)
        Payload (Subheader)                 (Must be 255)
        checksum (will be calculated from bus implementation!)
    '''
    result = bus.send_bytes_simple_message(bytes([dest,1,1,96,255]))
    if not result == True:
        #We need some better Failure Handling
        print("Error", result, "during enter programming mode")
        return False

    '''
    We need to send the data.  
    We need to read the file and write date in a loop ->
        Read package_size of bytes from the file. 
        Write the bytes to the validator.     
    '''
    sent = 0
    file_bytes = 1
    file_size = os.stat(file).st_size
    with open(file, 'rb') as bin_file:
        while file_bytes:
            file_bytes = bin_file.read(200)
            if len(file_bytes)>0: #We need this to not send any empty message
                sent += len(file_bytes)
                '''
                Message:
                    dest address
                    number of data bytes + 1 (the 1 is the subheader number)
                    source address
                    header 
                    payload:
                        subheader
                        databytes
                    checksum (will be calculated from bus implementation!)
                '''
                message = bytes([2,len(file_bytes)+1,1,96,254])+file_bytes
                result = bus.send_bytes_simple_message(message)
                if not result == True:
                    print ("Error", result, "during programming")
                    return False
                #print(len(file_bytes), message, ccTalk_Message.make_simple_checksum_for_bytes(message))
    if sent != file_size:
        print ("Error during file read")
        return False

    '''
    Finalize the upload. Send the endpacket programm header.
    '''
    result = bus.send_bytes_simple_message(bytes([dest,2,1,96,253,channel]))
    if not result == True:
        #We need some better Failure Handling
        print("Error", result, "saving data")
        return False
    time.sleep(2)
    return True

def rcp_erase_coin_channel(bus:ccTalk_Bus,dest:int, channel:int):
    print ("Erasing channel",channel)
    '''
    Set the validator into programming mode. -> if no ack no action
    Message to reach programming mode is:
        Destination adddress                
        Payload Size/Number of data bytes   (1, as we use a sub header)
        Source  address                     (1, as we are the master)
        Header                              (Must be 96)
        Payload (Subheader)                 (Must be 255)
        checksum (will be calculated from bus implementation!)
    '''
    result = bus.send_bytes_simple_message(bytes([dest,2,1,96,249,channel]))
    if result != True:
        #We need some better Failure Handling
        print("Error",result, "during removal of coins")
        return False
    time.sleep(2)
    return True
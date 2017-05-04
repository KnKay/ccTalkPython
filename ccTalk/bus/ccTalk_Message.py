'''
We define a class of ccTalk_Message. 

'''


class ccTalk_Message:

    @staticmethod
    def verify_from_bytes(message):
        if not ((type(message) is bytes) or (type(message) is ccTalk_Message)):
            return False
        #Check if the length is matching
        if not len(ccTalk_Message.get_payload_from_bytes(message)) == int(message[1]):
            return False
        #If we have a return header different to 0 we return the failure
        return True

    #USe this method if you can things different to an ack.
    @staticmethod
    def verify_answer_bytes(message):
        if not ((type(message) is bytes) or (type(message) is ccTalk_Message)):
            return False
        #Check if the length is matching
        if not len(ccTalk_Message.get_payload_from_bytes(message)) == int(message[1]):
            return False
        #We have a failure code if we have a payload!
        if message[1] != 0 :
            return message[4]
        return True

    @staticmethod
    def get_payload_from_bytes(bytes:bytes):
        if bytes[1] == 0:
            return []
        return bytes[4:-1] #return a sub array holding the payload

    @staticmethod
    def verify_simple_checksum_from_bytes(bytes:bytes):
        #Add all numbers
        value = 0
        for byte in bytes:
            value = value+byte
        value = value%256
        if value is 0:
            return True
        return False

    @staticmethod
    def make_simple_checksum_for_bytes(bytes:bytes):
        #Add all numbers
        value = 0
        for byte in bytes:
            value = value+byte
        return 256 - (value % 256)

    @staticmethod
    def simple_checksum_from_bytes(bytes:bytes):
        #Add all numbers
        value = 0
        for byte in bytes:
            value = value+byte
        value = value%256
        if value is 0:
            return True
        return False

    @classmethod
    def from_bytes(cls, bytes):
        payload = ccTalk_Message.get_payload_from_bytes(bytes)
        if bytes[1] != len(payload):
            return False
        dest = bytes[0]
        src = bytes[2]
        header = bytes[3]
        return ccTalk_Message(src,dest,header,payload)


    def __init__(self, src:int=1, dest:int=2, header:int=0, payload=bytes, checksum:int=0):
        self.__payload = payload
        self.__no_of_bytes = len(payload)
        self.__src = src
        self.__dest = dest
        self.__header = header


    def __bytes__(self):
        data_array = [self.dest,self.__no_of_bytes,self.src,self.header]
        for byte in self.payload:
            data_array.append(byte)
        data_array.append(self.checksum)
        as_bytes = bytes(data_array)
        return as_bytes


    #Setter and getter
    @property
    def payload(self):
        return self.__payload

    @property
    def src(self):
        return self.__src

    @property
    def dest(self):
        return self.__dest

    @property
    def header(self):
        return self.__header

    @property
    def checksum(self):
        value = 0
        value += self.dest
        value += self.__no_of_bytes
        value += self.src
        value += self.header
        for byte in self.payload:
            value = value + byte
        return 256-(value % 256)

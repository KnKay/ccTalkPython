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
        return True

    @staticmethod
    def get_payload_from_bytes(bytes:bytes):
        if bytes[1] == 0:
            return []
        return bytes[3:-2] #return a sub array holding the payload

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


    def __init__(self, src:int=1, dest:int=2,payload=bytes):
        self.__payload = payload
        self.__src = src
        self.__dest = dest

    def __bytes__(self):
        pass

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
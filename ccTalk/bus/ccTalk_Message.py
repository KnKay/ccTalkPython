'''
We define a class of ccTalk_Message. 



'''


class ccTalk_Message:

    @staticmethod
    def verify(message):
        if not type(message) == ccTalk_Message:
            return False
        return True
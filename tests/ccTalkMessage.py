import unittest
from ccTalk.bus.ccTalk_Message import ccTalk_Message

class ccTalk_Message_Test(unittest.TestCase):

    def test_getBytesPayload(self):
        test_message = bytes([2, 2, 1, 245, 13, 14, 8])
        payload = ccTalk_Message.get_payload_from_bytes(test_message)
        self.assertTrue(True)

    def test_verify(self):
        test_message = bytes([ 2, 0, 1, 245, 8])
        self.assertTrue(ccTalk_Message.verify_from_bytes(test_message))

    def test_bytes_checksum(self):
        #Testing with know good demo message
        test_message = bytes([2, 0, 1, 245, 8])
        self.assertTrue(ccTalk_Message.verify_simple_checksum_from_bytes(test_message))

    def test_from_bytes(self):
        test_message_bytes = bytes([2, 0, 1, 241, 12])
        test_message = ccTalk_Message.from_bytes(test_message_bytes)
        self.assertTrue(type(test_message)==ccTalk_Message)
        self.assertEqual(test_message.src, 1)
        self.assertEqual(bytes(test_message),test_message_bytes )
        #Test checksum creation once again for simple checksum
        test_message_bytes = bytes([2, 0, 1, 229, 24])
        self.assertEqual(bytes(ccTalk_Message.from_bytes(test_message_bytes)), test_message_bytes)
        test_message_bytes = bytes([2, 0, 1, 245, 8])
        self.assertEqual(bytes(ccTalk_Message.from_bytes(test_message_bytes)), test_message_bytes)



if __name__ == '__main__':
    unittest.main()
import unittest
from ccTalk.bus.ccTalk_Message import ccTalk_Message

class ccTalk_Message_Test(unittest.TestCase):

    def test_getBytesPayload(self):
        testMessage = bytes([2, 2, 1, 245, 13, 14, 8])
        payload = ccTalk_Message.get_payload_from_bytes(testMessage)
        self.assertTrue(True)

    def test_verify(self):
        testMessage = bytes([ 2, 0, 1, 245, 8])
        self.assertTrue(ccTalk_Message.verify_from_bytes(testMessage))

    def test_bytes_checksum(self):
        testMessage = bytes([2, 0, 1, 245, 8])
        self.assertTrue(ccTalk_Message.verify_simple_checksum_from_bytes(testMessage))


if __name__ == '__main__':
    unittest.main()
import unittest
from ccTalk.bus.ccTalk_Bus import ccTalk_Bus, ccTalk_Message
testPort="COM4"

class ccTalk_Bus_Test(unittest.TestCase):

    portUnderTest = ccTalk_Bus.by_port_name(testPort)
    #Test the by name function which allows singleton
    def test_singleton(self):
        self.assertEqual(ccTalk_Bus.by_port_name("port1"), ccTalk_Bus.by_port_name("port1"))
        self.assertNotEqual(ccTalk_Bus.by_port_name("port1"), ccTalk_Bus.by_port_name("port12"))


    def test_initialization(self):
        self.assertFalse(self.portUnderTest.is_initialized)
        self.assertTrue(self.portUnderTest.initialize())
        self.assertTrue(self.portUnderTest.is_initialized)

    def test_open_close(self):
        self.assertFalse(self.portUnderTest.is_open)
        self.assertTrue(self.portUnderTest.open())
        self.assertTrue(self.portUnderTest.is_open)
        self.assertTrue(self.portUnderTest.close())
        self.assertFalse(self.portUnderTest.is_open)

    #This will only work with any unit attached
    def test_sending_simple(self):
        test_message = ccTalk_Message.from_bytes(bytes([2, 0, 1, 254]))
        if not self.portUnderTest.open():
            self.portUnderTest.open()
        self.assertTrue(self.portUnderTest.send_cctalk_simple_message(test_message))
        self.assertTrue(self.portUnderTest.send_bytes_simple_message(bytes(test_message)))
        self.portUnderTest.close()


    #This will only work with the correct unit attached!
    def test_sending_request(self):
        if not self.portUnderTest.open():
            self.portUnderTest.open()
        test_message = ccTalk_Message.from_bytes(bytes([2, 0, 1, 245])) #Read equipment
        self.assertEqual(self.portUnderTest.send_cctalk_request_message(test_message).__bytes__(),self.portUnderTest.send_bytes_request_message(bytes(test_message) ))
        self.assertEqual(self.portUnderTest.send_cctalk_request_message(test_message).payload.decode("UTF-8"), "Coin Acceptor")
        self.portUnderTest.close()



if __name__ == '__main__':
    unittest.main()
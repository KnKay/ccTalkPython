import unittest
from ccTalk.bus.ccTalk_Bus import ccTalk_Bus
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


if __name__ == '__main__':
    unittest.main()
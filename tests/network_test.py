import unittest
from colorama import *

from network.network_manager import Network, Ip

init()


class ColoredTestResult(unittest.TextTestResult):

    COLOR_OK = Fore.GREEN  # Green
    COLOR_FAILURE = Fore.RED  # Red
    COLOR_ERROR = Fore.RED  # Red
    COLOR_RESET = Fore.RESET  # Reset format

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f"{self.COLOR_OK}All tests passed! Great job!{self.COLOR_RESET}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"{self.COLOR_FAILURE}Test failed! Please check the implementation.{self.COLOR_RESET}")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"{self.COLOR_ERROR}Oops! An error occurred during the test.{self.COLOR_RESET}")


class TestIPNetwork(unittest.TestCase):
    def test_ip_to_int(self):
        ip = Ip('192.168.1.1')
        self.assertEqual(ip.value, 3232235777)

    def test_int_to_ip(self):
        self.assertEqual(Ip.int_to_cidr(3232235777), '192.168.1.1')

    def test_cidr_to_netmask(self):
        network = Network('192.168.1.0', 24)
        self.assertEqual(network.mask, 4294967040)  # 255.255.255.0 in int

    def test_get_ip(self):
        network = Network('192.168.1.0', 24)
        self.assertEqual(network.get_ip(), '192.168.1.0')

    def test_get_mask(self):
        network = Network('192.168.1.0', 24)
        self.assertEqual(network.get_mask(), 4294967040)  # 255.255.255.0 in int

    def test_get_mask_dotted(self):
        network = Network('192.168.1.0', 24)
        self.assertEqual(network.get_mask_dotted(), '255.255.255.0')

    def test_in_network_true(self):
        network = Network('192.168.1.0', 24)
        self.assertTrue(network.in_network('192.168.1.15'))

    def test_in_network_false(self):
        network = Network('192.168.1.0', 24)
        self.assertFalse(network.in_network('192.168.2.15'))

    def test_in_network_border(self):
        network = Network('192.168.1.0', 24)
        self.assertTrue(network.in_network('192.168.1.0'))  # Border case
        self.assertTrue(network.in_network('192.168.1.255'))  # Border case

    def test_in_network_outside(self):
        network = Network('192.168.1.0', 24)
        self.assertFalse(network.in_network('192.168.0.255'))  # Outside case
        self.assertFalse(network.in_network('192.168.2.0'))  # Outside case


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=ColoredTestResult))

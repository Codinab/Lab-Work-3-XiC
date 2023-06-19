import unittest

from network.network_classes.Ip import Ip


class TestIp(unittest.TestCase):

    def test_octets_to_int(self):
        self.assertEqual(Ip('192.168.1.1').value, 3232235777)
        self.assertEqual(Ip('0.0.0.0').value, 0)
        self.assertEqual(Ip('255.255.255.255').value, 4294967295)
        self.assertEqual(Ip('127.0.0.1').value, 2130706433)
        self.assertEqual(Ip('8.8.8.8').value, 134744072)

    def test_int_to_octets(self):
        self.assertEqual(Ip('192.168.1.1').int_to_octets(3232235777), '192.168.1.1')
        self.assertEqual(Ip('0.0.0.0').int_to_octets(0), '0.0.0.0')
        self.assertEqual(Ip('255.255.255.255').int_to_octets(4294967295), '255.255.255.255')
        self.assertEqual(Ip('127.0.0.1').int_to_octets(2130706433), '127.0.0.1')
        self.assertEqual(Ip('8.8.8.8').int_to_octets(134744072), '8.8.8.8')

    def test_str(self):
        self.assertEqual(str(Ip('192.168.1.1')), '192.168.1.1')
        self.assertEqual(str(Ip('0.0.0.0')), '0.0.0.0')
        self.assertEqual(str(Ip('255.255.255.255')), '255.255.255.255')
        self.assertEqual(str(Ip('127.0.0.1')), '127.0.0.1')
        self.assertEqual(str(Ip('8.8.8.8')), '8.8.8.8')

    def test_eq(self):
        self.assertTrue(Ip('192.168.1.1') == Ip('192.168.1.1'))
        self.assertFalse(Ip('192.168.1.1') == Ip('192.168.1.2'))
        self.assertTrue(Ip('0.0.0.0') == Ip('0.0.0.0'))
        self.assertFalse(Ip('0.0.0.0') == Ip('255.255.255.255'))
        self.assertTrue(Ip('8.8.8.8') == Ip('8.8.8.8'))

    def test_lt(self):
        self.assertTrue(Ip('192.168.1.1') < Ip('192.168.1.2'))
        self.assertFalse(Ip('192.168.1.2') < Ip('192.168.1.1'))
        self.assertTrue(Ip('0.0.0.0') < Ip('255.255.255.255'))
        self.assertFalse(Ip('255.255.255.255') < Ip('0.0.0.0'))
        self.assertTrue(Ip('8.8.4.4') < Ip('8.8.8.8'))


if __name__ == '__main__':
    unittest.main()

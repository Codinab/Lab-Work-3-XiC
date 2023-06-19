import unittest

from network.network_classes.Netmask import Netmask


class TestNetmask(unittest.TestCase):

    def test_cidr_to_int(self):
        self.assertEqual(Netmask('255.255.255.0').netmask, 4294967040)
        self.assertEqual(Netmask('255.255.0.0').netmask, 4294901760)
        self.assertEqual(Netmask('255.0.0.0').netmask, 4278190080)
        self.assertEqual(Netmask('0.0.0.0').netmask, 0)
        self.assertEqual(Netmask('128.0.0.0').netmask, 2147483648)

    def test_int_to_cidr(self):
        self.assertEqual(Netmask('255.255.255.0').int_to_cidr(4294967040), '255.255.255.0')
        self.assertEqual(Netmask('255.255.0.0').int_to_cidr(4294901760), '255.255.0.0')
        self.assertEqual(Netmask('255.0.0.0').int_to_cidr(4278190080), '255.0.0.0')
        self.assertEqual(Netmask('0.0.0.0').int_to_cidr(0), '0.0.0.0')
        self.assertEqual(Netmask('128.0.0.0').int_to_cidr(2147483648), '128.0.0.0')

    def test_netmask_to_decimal(self):
        self.assertEqual(Netmask('255.255.255.0').netmask_to_decimal(), '255.255.255.0')
        self.assertEqual(Netmask('255.255.0.0').netmask_to_decimal(), '255.255.0.0')
        self.assertEqual(Netmask('255.0.0.0').netmask_to_decimal(), '255.0.0.0')
        self.assertEqual(Netmask('0.0.0.0').netmask_to_decimal(), '0.0.0.0')
        self.assertEqual(Netmask('128.0.0.0').netmask_to_decimal(), '128.0.0.0')

    def test_wildcard_to_decimal(self):
        self.assertEqual(Netmask('255.255.255.0').wildcard_to_decimal(), '0.0.0.255')
        self.assertEqual(Netmask('255.255.0.0').wildcard_to_decimal(), '0.0.255.255')
        self.assertEqual(Netmask('255.0.0.0').wildcard_to_decimal(), '0.255.255.255')
        self.assertEqual(Netmask('0.0.0.0').wildcard_to_decimal(), '255.255.255.255')
        self.assertEqual(Netmask('128.0.0.0').wildcard_to_decimal(), '127.255.255.255')

    def test_netmask_to_cidr(self):
        self.assertEqual(Netmask('255.255.255.0').netmask_to_cidr(), 24)
        self.assertEqual(Netmask('255.255.0.0').netmask_to_cidr(), 16)
        self.assertEqual(Netmask('255.0.0.0').netmask_to_cidr(), 8)
        self.assertEqual(Netmask('0.0.0.0').netmask_to_cidr(), 0)
        self.assertEqual(Netmask('128.0.0.0').netmask_to_cidr(), 1)

    def test_wildcard_to_cidr(self):
        self.assertEqual(Netmask('255.255.255.0').wildcard_to_cidr(), 8)
        self.assertEqual(Netmask('255.255.0.0').wildcard_to_cidr(), 16)
        self.assertEqual(Netmask('255.0.0.0').wildcard_to_cidr(), 24)
        self.assertEqual(Netmask('0.0.0.0').wildcard_to_cidr(), 32)
        self.assertEqual(Netmask('128.0.0.0').wildcard_to_cidr(), 31)

    def test_is_host_mask(self):
        self.assertFalse(Netmask('255.255.255.0').is_host_mask())
        self.assertFalse(Netmask('255.255.0.0').is_host_mask())
        self.assertFalse(Netmask('255.0.0.0').is_host_mask())
        self.assertFalse(Netmask('0.0.0.0').is_host_mask())
        self.assertTrue(Netmask('255.255.255.255').is_host_mask())

    def test_is_default_mask(self):
        self.assertFalse(Netmask('255.255.255.0').is_default_mask())
        self.assertFalse(Netmask('255.255.0.0').is_default_mask())
        self.assertFalse(Netmask('255.0.0.0').is_default_mask())
        self.assertTrue(Netmask('0.0.0.0').is_default_mask())
        self.assertFalse(Netmask('255.255.255.255').is_default_mask())

    def test_eq(self):
        self.assertEqual(Netmask('255.255.255.0'), Netmask('255.255.255.0'))
        self.assertNotEqual(Netmask('255.255.255.0'), Netmask('255.255.0.0'))
        self.assertNotEqual(Netmask('255.255.255.0'), Netmask('255.0.0.0'))
        self.assertNotEqual(Netmask('255.255.255.0'), Netmask('0.0.0.0'))
        self.assertNotEqual(Netmask('255.255.255.0'), Netmask('128.0.0.0'))

if __name__ == '__main__':
    unittest.main()
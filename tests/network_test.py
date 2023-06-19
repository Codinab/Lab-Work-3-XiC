import unittest
from ipaddress import IPv4Network

from network.network_classes.Ip import Ip
from network.network_classes.Netmask import Netmask
from network.network_classes.Network import Network


class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.ip = Ip('192.168.0.1')
        self.netmask = Netmask('255.255.255.0')
        self.network = Network(self.ip, self.netmask)

    def test_get_ip(self):
        self.assertEqual(self.network.get_ip(), '192.168.0.1')

    def test_get_mask(self):
        self.assertEqual(self.network.get_mask(), self.netmask)

    def test_get_hosts(self):
        self.assertListEqual(self.network.get_hosts(), [])
        host1 = Ip('192.168.0.2')
        self.network.add_host(host1)
        self.assertListEqual(self.network.get_hosts(), [host1])

    def test_add_host(self):
        host2 = Ip('192.168.0.3')
        self.network.add_host(host2)
        self.assertIn(host2, self.network.get_hosts())

    def test_in_network(self):
        host3 = Ip('192.168.0.4')
        self.network.add_host(host3)
        self.assertTrue(self.network.in_network(host3))
        host4 = Ip('192.168.0.5')
        self.assertFalse(self.network.in_network(host4))

    def test_translate_to_net(self):
        network_address = Network.translate_to_net(Ip('192.168.0.2'), Netmask('255.255.255.0'))
        self.assertEqual(network_address, Ip('192.168.0.0'))

    def test_str(self):
        self.assertEqual(str(self.network), 'Network: 192.168.0.1/24')

    def test_eq(self):
        other_network = Network(Ip('192.168.0.1'), Netmask('255.255.255.0'))
        self.assertEqual(self.network, other_network)
        other_network = Network(Ip('192.168.0.2'), Netmask('255.255.255.0'))
        self.assertNotEqual(self.network, other_network)

if __name__ == '__main__':
    unittest.main()

import unittest

from network.network_classes.Ip import Ip
from network.network_classes.Netmask import Netmask
from network.network_classes.Network import Network
from network.network_classes.Router import Router, RouterInterface


class TestRouter(unittest.TestCase):

    def setUp(self):
        self.ip = Ip('192.168.0.1')
        self.router = Router(self.ip)
        self.interface_name = "eth0"
        self.interface_ip = Ip('192.168.0.2')
        self.interface_netmask = Netmask('255.255.255.0')
        self.interface_network = Network(self.interface_ip, self.interface_netmask)
        self.interface_speed = 100
        self.router_interface = RouterInterface(self.interface_name, self.interface_ip, self.interface_network,
                                                self.interface_speed)

    def test_add_interface(self):
        self.router.add_interface(self.router_interface)
        self.assertIn(self.router_interface, self.router.get_interfaces())

    def test_get_interfaces(self):
        self.router.add_interface(self.router_interface)
        self.assertListEqual(self.router.get_interfaces(), [self.router_interface])

    def test_get_ips(self):
        self.router.add_interface(self.router_interface)
        self.assertListEqual(self.router.get_ips(), [self.interface_ip])

    def test_add_route(self):
        route = (self.interface_network, self.interface_ip, "local")
        self.router.add_route(route)
        self.assertIn(route, self.router.get_routing_table())

    def test_get_networks(self):
        self.router.add_interface(self.router_interface)
        self.assertListEqual(self.router.get_networks(), [self.interface_network])

    def test_eq(self):
        router2 = Router(self.ip)
        router2.name = self.router.name
        self.assertEqual(self.router, router2)

    def test_get_other_hosts(self):
        host = Router(Ip('10.0.0.9'))
        host.name = "host"
        self.router_interface.network.add_host(host)
        self.assertEqual(self.router_interface.get_other_hosts(self.router), [host])


if __name__ == '__main__':
    unittest.main()

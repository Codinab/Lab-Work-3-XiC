import ipaddress

from network.network_classes.Ip import Ip
from network.network_classes.Netmask import Netmask


class Network:
    def __init__(self, ip: Ip, netmask: Netmask):
        self.ip = ip
        self.mask = netmask
        self.hosts = []

    def get_ip(self):
        return Ip.int_to_octets(self.ip.value)

    def get_mask(self) -> Netmask:
        """Returns the network mask in integer format."""
        return self.mask

    def get_hosts(self) -> list:
        return self.hosts

    def add_host(self, host):
        if host not in self.hosts:
            self.hosts.append(host)

    def in_network(self, ip: Ip):
        """Checks if the provided IP is within the network."""
        return self.hosts.count(ip) > 0

    @staticmethod
    def translate_to_net(ip_address: Ip, subnet_mask: Netmask):
        ip_network = ipaddress.IPv4Network(str(ip_address) + '/' + str(subnet_mask.netmask_to_cidr()), strict=False)
        network_address = str(ip_network.network_address)
        return Ip(network_address)

    def __str__(self):
        return "Network: " + Ip.int_to_octets(self.ip.value) + '/' + str(self.mask.netmask_to_cidr())

    def __eq__(self, other):
        return self.ip == other.ip and self.mask == other.mask

    def __hash__(self):
        return hash((self.ip, self.mask))
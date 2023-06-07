from easysnmp import Session


# https://easysnmp.readthedocs.io/en/latest/

class RouterInterface:
    def __init__(self, name, ip, mask):
        self.name = name
        self.ip = ip
        self.mask = mask


class Ip:
    def __init__(self, ip):
        self.value = self.octets_to_int(ip)

    @staticmethod
    def octets_to_int(ip):
        """Converts a dotted decimal format IP to integer."""
        octets = map(int, ip.split('.'))
        return sum(octet << (24 - i * 8) for i, octet in enumerate(octets))

    @staticmethod
    def int_to_octets(ip):
        """Converts an integer IP to dotted decimal format."""
        return '.'.join(str(ip >> (24 - i * 8) & 0xFF) for i in range(4))

    def __str__(self):
        return self.int_to_octets(self.value)


class Netmask:
    def __init__(self, mask):
        self.netmask = self.cidr_to_int(mask)
        self.wildcard = self.cidr_to_int(self.int_to_cidr(~self.netmask))

    @staticmethod
    def cidr_to_int(mask):
        """Converts a dotted decimal format IP to integer."""
        octets = map(int, mask.split('.'))
        return sum(octet << (24 - i * 8) for i, octet in enumerate(octets))

    @staticmethod
    def int_to_cidr(mask):
        """Converts an integer IP to dotted decimal format."""
        return '.'.join(str(mask >> (24 - i * 8) & 0xFF) for i in range(4))

    def netmask_to_decimal(self):
        """Converts a netmask to dotted decimal format."""
        return self.int_to_cidr(self.netmask)

    def wildcard_to_decimal(self):
        """Converts a wildcard to dotted decimal format."""
        return self.int_to_cidr(self.wildcard)

    def netmask_to_cidr(self):
        """Converts a netmask to CIDR notation."""
        return sum(bin(int(x)).count('1') for x in self.int_to_cidr(self.netmask).split('.'))

    def wildcard_to_cidr(self):
        """Converts a wildcard to CIDR notation."""
        return sum(bin(int(x)).count('1') for x in self.int_to_cidr(self.wildcard).split('.'))


class Router:
    def __init__(self, name: str, ip: Ip):
        self.name = name
        self.ip = ip
        self.interfaces = []
        self.networks = []
        self.routing_table = []

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def get_interfaces(self):
        return self.interfaces

    def get_networks(self):
        return self.networks

    def get_routing_table(self):
        return self.routing_table

    def add_network(self, network):
        self.networks.append(network)

    def add_route(self, route):
        self.routing_table.append(route)

    def is_neighbor(self, router):
        for network in self.networks:
            for network2 in router.get_networks():
                if network == network2:
                    return True
        return False

    def __eq__(self, other):
        return self.name == other.name


class Network:
    def __init__(self, ip: Ip, netmask: Netmask):
        self.ip = ip
        self.mask = netmask

    def get_ip(self):
        return Ip.int_to_octets(self.ip.value)

    def get_mask(self) -> Netmask:
        """Returns the network mask in integer format."""
        return self.mask

    def in_network(self, ip):
        """Checks if the provided IP is within the network."""





class NetworkManager:
    ROUTE_NETWORK_OID = "IP-FORWARD-MIB::ipCidrRouteDest"
    ROUTE_MASK_OID = "IP-FORWARD-MIB::ipCidrRouteMask"
    ROUTE_NEXT_HOP_OID = "IP-FORWARD-MIB::ipCidrRouteNextHop"
    ROUTE_TYPE_OID = "IP-FORWARD-MIB::ipCidrRouteType"

    def __init__(self, access_ip, community):
        self.ip = Ip(access_ip)
        self.community = community
        self.access_router = Router(self.get_sysname(self.ip), self.ip)
        self.set_routing_table(self.access_router)
        self.print_routing_table(self.access_router.routing_table)

    @staticmethod
    def get_sysname(ip: Ip, community='rocom'):
        session = Session(hostname=str(ip), community=community, version=2)
        sysname = session.get('sysName.0')
        return sysname

    def set_routing_table(self, router: Router):
        session = Session(hostname=str(router.ip), community=self.community, version=2)

        routes = session.walk(self.ROUTE_NETWORK_OID)
        for route in routes:
            destination = Ip(route.value)
            netmask = Netmask(session.get(f'{self.ROUTE_MASK_OID}.{route.oid_index}').value)
            network = Network(destination, netmask)
            next_hop = Ip(session.get(f'{self.ROUTE_NEXT_HOP_OID}.{route.oid_index}').value)

            router.routing_table.append((network, next_hop))
        return router.routing_table

    @staticmethod
    def print_router_info(sysname, ips):
        print(f"SysName: {sysname}")
        print("IPs:")
        for ip, data in ips.items():
            print(f"IP: {ip}, Netmask: {data['Netmask']}, Speed: {data['Speed']}, Status: {data['Status']}")

    @staticmethod
    def print_routing_table(routing_table):
        print("Routing Table:")
        for network, nexthop in routing_table:
            print(f"Network: {network.get_ip():15} Netmask: {network.get_mask().netmask_to_decimal():15} Next hop: {nexthop}")


if __name__ == '__main__':
    network_manager = NetworkManager('10.0.0.2', 'rocom')

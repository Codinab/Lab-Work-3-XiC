from easysnmp import Session


# https://easysnmp.readthedocs.io/en/latest/


class RouterInterface:
    def __init__(self, name, ip, network, speed):
        self.name = name
        self.network = network
        self.ip = ip
        self.speed = speed # in Mbps

    def __str__(self):
        return f"Name: {self.name}, Ip: {self.ip}, {self.network}, Speed: {self.speed} Mbps"


class Ip:
    def __init__(self, ip):
        self.value = self.octets_to_int(ip)

    @staticmethod
    def octets_to_int(ip):
        """Converts a dotted decimal format IP to integer."""
        octets = map(int, ip.split('.'))
        return sum(octet << (24 - i * 8) for i, octet in enumerate(octets))

    @staticmethod
    def int_to_octets(ip_value):
        """Converts an integer IP to dotted decimal format."""
        return '.'.join(str(ip_value >> (24 - i * 8) & 0xFF) for i in range(4))

    def __str__(self):
        return self.int_to_octets(self.value)

    def __eq__(self, other):
        return self.value == other.value


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

    def is_host_mask(self):
        """Checks if the netmask is a host mask."""
        return self.netmask == 0xFFFFFFFF

    def is_default_mask(self):
        """Checks if the netmask is a default mask."""
        return self.netmask == 0x00000000


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
        self.hosts = []

    def get_ip(self):
        return Ip.int_to_octets(self.ip.value)

    def get_mask(self) -> Netmask:
        """Returns the network mask in integer format."""
        return self.mask

    def get_hosts(self) -> list:
        return self.hosts

    def add_host(self, host: Ip):
        self.hosts.append(host)

    def in_network(self, ip: Ip):
        """Checks if the provided IP is within the network."""
        return self.hosts.count(ip) > 0


    def __str__(self):
        return "Network: " + Ip.int_to_octets(self.ip.value) + '/' + str(self.mask.netmask_to_cidr())


class NetworkManager:
    ROUTE_NETWORK_OID = "IP-FORWARD-MIB::ipCidrRouteDest"
    ROUTE_MASK_OID = "IP-FORWARD-MIB::ipCidrRouteMask"
    ROUTE_NEXT_HOP_OID = "IP-FORWARD-MIB::ipCidrRouteNextHop"
    ROUTE_TYPE_OID = "IP-FORWARD-MIB::ipCidrRouteType"
    IF_NAME_OID = "IF-MIB::ifName"
    IF_DESCR_OID = "IF-MIB::ifDescr"
    IF_SPEED_OID = "IF-MIB::ifSpeed"
    IP_ADDR_OID = "IP-MIB::ipAdEntAddr"
    IP_MASK_OID = "IP-MIB::ipAdEntNetMask"

    def __init__(self, access_ip, community):
        self.ip = Ip(access_ip)
        self.community = community
        self.routers_in_network = []
        self.networks = {}

        self.access_router = Router(self.get_sysname(self.ip), self.ip)
        self.routers_in_network.append(self.access_router)

        self.set_routing_table(self.access_router)
        self.get_interfaces_info(self.access_router)
        for network in self.networks.values():
            print(network)

    def get_interfaces_info(self, router: Router):
        session = Session(hostname=str(router.ip), community=self.community, version=2)

        if_descr = session.walk(self.IF_DESCR_OID)
        if_speed = session.walk(self.IF_SPEED_OID)
        if_ip_address = session.walk(self.IP_ADDR_OID)
        if_ip_mask = session.walk(self.IP_MASK_OID)

        for i in range(len(if_ip_address)):
            # Skip down interfaces and loopback interfaces
            if if_descr[i].value.count('Vo') > 0 or if_descr[i].value.count('Nu') > 0:
                continue

            # Get the IP address and subnet mask for the interface
            ip = Ip(if_ip_address[i].value)
            mask = Netmask(if_ip_mask[i].value)

            # Translate the IP address and subnet mask to the network IP
            network_ip = self.translate_to_net(ip, mask)

            # Check if the network IP already exists in the network dictionary
            if self.networks.get(str(network_ip)) is None:
                # Create a new Network object for the network IP
                network = Network(network_ip, mask)

                # Add the new network to the networks dictionary
                self.networks[str(network_ip)] = network
            else:
                # Retrieve the existing network from the networks dictionary
                network = self.networks.get(network_ip)

            # Create a RouterInterface object with the interface details
            interface = RouterInterface(if_descr[i].value, ip, network, if_speed[i].value)

            # Add the interface to the router's interface list
            router.add_interface(interface)

            # Add the network to the router's network list
            router.add_network(network)

            # Add the IP address to the network's list of hosts
            network.add_host(ip)

    @staticmethod
    def get_sysname(ip: Ip, community='rocom'):
        session = Session(hostname=str(ip), community=community, version=2)
        sysname = session.get('sysName.0').value
        return sysname

    def set_routing_table(self, router: Router):
        session = Session(hostname=str(router.ip), community=self.community, version=2)
        routes = session.walk(self.ROUTE_NETWORK_OID)

        for route in routes:
            destination = Ip(route.value)
            netmask = Netmask(session.get(f'{self.ROUTE_MASK_OID}.{route.oid_index}').value)
            network = Network(destination, netmask)
            if not netmask.is_host_mask():
                router.add_network(network)
            next_hop = Ip(session.get(f'{self.ROUTE_NEXT_HOP_OID}.{route.oid_index}').value)


    # def set_interface(self, )

    def set_routing_table_old(self, router: Router):
        session = Session(hostname=str(router.ip), community=self.community, version=2)
        routes = session.walk(self.ROUTE_NETWORK_OID)
        for route in routes:
            destination = Ip(route.value)
            netmask = Netmask(session.get(f'{self.ROUTE_MASK_OID}.{route.oid_index}').value)
            network = Network(destination, netmask)
            next_hop = Ip(session.get(f'{self.ROUTE_NEXT_HOP_OID}.{route.oid_index}').value)

            if str(next_hop) != "0.0.0.0":
                sysname = self.get_sysname(next_hop)
                nexthope_router = Router(sysname, next_hop)
                add_router = True
                for router in self.routers_in_network:
                    if router.name == nexthope_router.name:
                        add_router = False
                        break

                if add_router == True:
                    self.routers_in_network.append(nexthope_router)
                    self.print_routers()
                    self.set_routing_table(nexthope_router)

            else:
                sysname = 'local'
            router.routing_table.append((network, next_hop, sysname))

        self.print_routing_table(router.routing_table, router.name)
        return router.routing_table

    def print_routers(self):
        print("The routers in the network are:", end=" ")
        router_names = [router.name for router in self.routers_in_network]
        print(*router_names, sep=", ")

    @staticmethod
    def print_router_info(sysname, ips):
        print(f"SysName: {sysname}")
        print("IPs:")
        for ip, data in ips.items():
            print(f"IP: {ip}, Netmask: {data['Netmask']}, Speed: {data['Speed']}, Status: {data['Status']}")

    @staticmethod
    def print_routing_table(routing_table, router_name=""):
        print("Routing Table of" + router_name + ":")
        for network, nexthop, sysname in routing_table:
            print(
                f"  Network: {network.get_ip():15} Netmask: {network.get_mask().netmask_to_decimal():15} Next hop: {nexthop} Sysname: {sysname}")


if __name__ == '__main__':
    network_manager = NetworkManager('10.0.0.2', 'rocom')

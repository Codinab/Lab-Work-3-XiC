from easysnmp import Session

from network.network_classes.Ip import Ip
from network.network_classes.Netmask import Netmask
from network.network_classes.Network import Network

ROUTE_NETWORK_OID = "IP-FORWARD-MIB::ipCidrRouteDest"
ROUTE_MASK_OID = "IP-FORWARD-MIB::ipCidrRouteMask"
ROUTE_NEXT_HOP_OID = "IP-FORWARD-MIB::ipCidrRouteNextHop"
ROUTE_TYPE_OID = "IP-FORWARD-MIB::ipCidrRouteType"
IF_NAME_OID = "IF-MIB::ifName"
IF_DESCR_OID = "IF-MIB::ifDescr"
IF_TYPE_OID = "IF-MIB::ifType"
IF_SPEED_OID = "IF-MIB::ifSpeed"
IP_ADDR_OID = "IP-MIB::ipAdEntAddr"
IP_MASK_OID = "IP-MIB::ipAdEntNetMask"

IF_NAME_OID = "IF-MIB::ifName"
IF_DESCR_OID = "IF-MIB::ifDescr"
IF_TYPE_OID = "IF-MIB::ifType"
IF_SPEED_OID = "IF-MIB::ifSpeed"
IP_ADDR_OID = "IP-MIB::ipAdEntAddr"
IP_MASK_OID = "IP-MIB::ipAdEntNetMask"
INTERFACE_INDEX_TO_ADDR_OID = "RFC1213-MIB::ipAdEntIfIndex"


class RouterInterface:
    def __init__(self, name, ip, network: Network, speed):
        self.name = name
        self.network = network
        self.ip = ip
        self.speed = speed  # in Mbps

    def __str__(self):
        return f"Name: {self.name}, Ip: {self.ip}, {self.network}, Speed: {self.speed} Mbps"


class Router:
    def __init__(self, ip: Ip):
        self.name = ""
        self.ip = ip
        self.interfaces = []
        self.routing_table = []

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def get_interfaces(self):
        return self.interfaces

    def add_route(self, route):
        self.routing_table.append(route)

    def get_networks(self):
        return [interface.network for interface in self.interfaces]

    def is_neighbor(self, router):
        for network in self.get_networks():
            for network2 in router.get_networks():
                if network == network2:
                    return True
        return False

    def get_interfaces_info(self, community):
        session = Session(hostname=str(self.ip), community=community, version=2)
        return list(
            map(
                lambda pair: self._get_interface_details(session, pair['index'], pair['addr']),
                self._interface_index_set_pairs(session),
            )
        )

    @staticmethod
    def _interface_index_set_pairs(session: Session):
        return list(
            map(
                lambda entry: {'index': entry.value, 'addr': entry.oid_index},
                session.walk(INTERFACE_INDEX_TO_ADDR_OID),
            )
        )

    def _get_interface_details(self, session: Session, index: str, addr: str):
        details = {
            "IF_DESCR": self._get_oid_value(session, IF_DESCR_OID, index),
            "IP_ADDRESS": addr,
            "IP_MASK": self._get_oid_value(session, IP_MASK_OID, addr),
            "IF_SPEED": self._get_oid_value(session, IF_SPEED_OID, index),
            "IF_TYPE": self._get_oid_value(session, IF_TYPE_OID, index),
        }
        # Add check for 'Vo' or 'Nu' in IF_DESCR if necessary



        # Create a RouterInterface and add it to the router
        ip = Ip(details["IP_ADDRESS"])
        mask = Netmask(details["IP_MASK"])
        network_ip = Network.translate_to_net(ip, mask)
        network = Network(network_ip, mask)
        interface = RouterInterface(details["IF_DESCR"], ip, network, details["IF_SPEED"])

        # Ignore loopback interfaces
        if details["IF_TYPE"] != "24":
            self.add_interface(interface)

        return details

    @staticmethod
    def _get_oid_value(session: Session, oid: str, index: str) -> str:
        return session.get(oid + "." + index).value

    def set_routing_table(self, community):
        session = Session(hostname=str(self.ip), community=community, version=2)
        routes = session.walk(ROUTE_NETWORK_OID)

        for route in routes:
            destination = Ip(route.value)
            netmask = Netmask(session.get(f'{ROUTE_MASK_OID}.{route.oid_index}').value)
            network = Network(destination, netmask)

            next_hop = Ip(session.get(f'{ROUTE_NEXT_HOP_OID}.{route.oid_index}').value)

            self.routing_table.append((network, next_hop))

    def get_known_routers(self, community):
        session = Session(hostname=str(self.ip), community=community, version=2)

        ospf_nbr_ip_oid = 'OSPF-MIB::ospfNbrIpAddr'

        # Retrieve the OSPF neighbor IP addresses
        ospf_nbr_ips = session.walk(ospf_nbr_ip_oid)

        # Retrieve the OSPF neighbor router IDs

        known_routers = []

        # Iterate over the retrieved information for each OSPF neighbor
        for i in range(len(ospf_nbr_ips)):
            nbr_ip = ospf_nbr_ips[i].value

            # Append the neighbor to the list of known routers
            known_routers.append(nbr_ip)

        return known_routers

    def get_routing_table(self):
        return self.routing_table

    def get_name(self, community):
        session = Session(hostname=str(self.ip), community=community, version=2)
        self.name = session.get('sysName.0').value

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f"Name: {self.name}, Interfaces: {[str(interface) for interface in self.interfaces]}"

from easysnmp import Session


class NetworkManager:
    def __init__(self, ip, community):
        self.ip = ip
        self.community = community
        self.session = Session(hostname=self.ip, community=self.community, version=2)

    def poll_router(self):
        sysname = self.session.get('sysName.0').value
        return sysname

    def get_ips(self):
        ips = {}
        interfaces = self.session.walk('ipAdEntIfIndex')
        for interface in interfaces:
            ip_address = interface.oid_index.replace('ipAdEntIfIndex.', '')
            netmask = self.session.get(f'ipAdEntNetMask.{ip_address}').value
            speed = self.session.get(f'ifSpeed.{interface.value}').value
            status = self.session.get(f'ifOperStatus.{interface.value}').value
            ips[ip_address] = {
                'Netmask': netmask,
                'Speed': speed,
                'Status': status
            }
        return ips

    def retrieve_routing_table(self):
        routing_table = []
        routes = self.session.walk('ipCidrRouteDest')
        for route in routes:
            destination = route.value
            netmask = self.session.get(f'ipCidrRouteMask.{route.oid_index}').value
            routing_table.append((destination, netmask))
        return routing_table

    @staticmethod
    def print_router_info(sysname, ips):
        print(f"SysName: {sysname}")
        print("IPs:")
        for ip, data in ips.items():
            print(f"IP: {ip}, Netmask: {data['Netmask']}, Speed: {data['Speed']}, Status: {data['Status']}")

    @staticmethod
    def print_routing_table(routing_table):
        print("Routing Table:")
        for destination, netmask in routing_table:
            print(f"Destination: {destination}, Netmask: {netmask}")

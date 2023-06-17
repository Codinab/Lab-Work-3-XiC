from easysnmp import Session
import ipaddress


# https://easysnmp.readthedocs.io/en/latest/


class NetworkManager:
    def __init__(self, access_ip, community):
        self.ip = Ip(access_ip)
        self.community = community
        self.networks = []

        self.access_router = Router(self.ip)
        self.access_router.get_name(self.community)

        # self.set_routing_table(self.access_router)
        # self.get_interfaces_info(self.access_router)

        self.access_router.get_interfaces_info(self.community)

        self.access_router.set_routing_table(self.community)

        self.access_router.get_interfaces()

        self.network_explorer = NetworkExplorer(self.access_router, self.community)
        self.routers = self.network_explorer.explore()

        self.networks = []
        self.set_networks()

    def print_networks(self):
        # Print networks and routers
        for network in self.networks:
            print(f"Network: {network}")
            for router in network.hosts:
                print(f"  {router}")

    # def get_shortest_path(src_ip, dst_ip):
    #    src_ip = Ip(src_ip)
    #    dst_ip = Ip(dst_ip)
    #
    #    for subnet, next_hops in routing_tables.items():
    #        if src_ip in subnet and dst_ip in subnet:
    #            path = f"{src_ip}:{next_hops[0]}"
    #            for i in range(len(next_hops) - 1):
    #                path += f" → {next_hops[i + 1]}:{dst_ip}"
    #            return path
    #
    #    return "No route found"
    #
    def print_routers(self):
        print("The routers in the network are:")
        for router in self.routers:
            print(f"  {router}")

    def print_networks(self):
        for network in self.networks:
            print(f"Network: {network}")
            for host in network.get_hosts():
                print(host.name, end=" ")
            print()

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

    def set_networks(self):
        network_mapping = {}

        for router in self.routers:
            for interface in router.get_interfaces():
                network = interface.network

                if network not in network_mapping:
                    network_mapping[network] = network
                else:
                    interface.network = network_mapping[network]

        # Remove duplicate networks
        self.networks = list(set(network_mapping.values()))

        for router in self.routers:
            for interface in router.get_interfaces():
                network = interface.network
                network.add_host(router)




if __name__ == '__main__':
    network_manager = NetworkManager('10.0.0.2', 'rocom')

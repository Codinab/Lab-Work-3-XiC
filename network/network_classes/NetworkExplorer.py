from network.network_classes.Ip import Ip
from network.network_classes.Router import Router


class NetworkExplorer:
    def __init__(self, router: Router, community):
        self.routers = []
        self.community = community
        self.routers.append(router)

    def explore(self):
        self.__explore_router__(self.routers[0])
        return self.routers

    def __explore_router__(self, router: Router):
        for neighbor_router_ips in router.get_known_routers(self.community):
            router_found = Router(Ip(neighbor_router_ips))
            router_found.get_name(self.community)

            if router_found in self.routers:
                continue

            router_found.get_interfaces_info(self.community)
            router_found.set_routing_table(self.community)
            self.routers.append(router_found)
            self.__explore_router__(router_found)

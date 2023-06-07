from network.management import NetworkManager
from network.topology import NetworkTopology
from routing.summarization import RouteSummarizer


def main():
    # Dades de configuració
    router_ip = '192.168.0.1'
    community_string = 'rocom'

    network_manager = NetworkManager(router_ip, community_string)
    sysname = network_manager.poll_router()
    ips = network_manager.get_ips()
    network_manager.print_router_info(sysname, ips)

    routing_table = network_manager.retrieve_routing_table()
    network_manager.print_routing_table(routing_table)

    route_summarizer = RouteSummarizer(routing_table)
    route_summaries = route_summarizer.create_route_summaries()
    route_summarizer.print_route_summaries(route_summaries)

    network_topology = NetworkTopology()
    network_topology.add_router(sysname)
    network_topology.add_connection('Router1', 'Router2')
    network_topology.add_connection('Router2', 'Router3')
    network_topology.plot_topology()


if __name__ == '__main__':
    main()

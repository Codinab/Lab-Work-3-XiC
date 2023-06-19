import argparse
from network.network_manager import NetworkManager
from easysnmp import Session
from network.network_plot_maker.plot_maker import draw_network_map


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('router_ip', nargs='?', help="Router's IP")
    parser.add_argument('--community-string', '-c', help="Community string", default='rocom')
    parser.add_argument('--print-networks', '-n', action='store_true', help="Print networks")
    parser.add_argument('--print-routers', '-r', action='store_true', help="Print routers")
    parser.add_argument('--create-network-graph', '-g', action='store_true', help="Create network graph")
    parser.add_argument('--graph-file', default='', help="File name (Default=network_map)")
    parser.add_argument('--all', '-a', action='store_true', help="Execute all actions")
    parser.add_argument('--path', '-p', nargs=2, metavar=('ORIGIN', 'DEST'), help="Find the shortest path between two ips")


    args = parser.parse_args()

    if not args.router_ip and not args.all:
        parser.error("Router's IP is required or use --all option")

    if args.all:
        args.print_networks = True
        args.print_routers = True
        args.create_network_graph = True

    nm = NetworkManager(args.router_ip, args.community_string)

    if args.print_networks:
        nm.print_networks()

    if args.print_routers:
        nm.print_routers()

    if args.create_network_graph:
        draw_network_map(nm, args.graph_file)

    if args.path:
        path = nm.get_shortest_path(args.path[0], args.path[1])
        print([router.name for router in path])


if __name__ == '__main__':
    main()

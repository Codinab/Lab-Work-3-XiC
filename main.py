from network.network_manager import *
from easysnmp import Session


def main():
    router_ip = input('Router\'s IP: ')
    community_string = input('Community string: ')

    if router_ip == '':
        exit("No IP has been entered.")
    if community_string == '':
        exit("No community string has been entered.")

    network_manager = NetworkManager(router_ip, community_string)
    print(network_manager.set_routing_table())


if __name__ == '__main__':
    main()

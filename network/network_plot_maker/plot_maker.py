import networkx as nx
import matplotlib.pyplot as plt

from network.network_manager import NetworkManager


def draw_network_map(network_manager: NetworkManager, graph_file):
    G = nx.Graph()
    switches = {}
    switches_count = 0

    # Add nodes (routers) to the graph
    for router in network_manager.routers:
        interfaces_str = "\n".join([interface.name_speed() for interface in router.get_interfaces()])
        G.add_node(router.name, label=f"{router.name}\n{interfaces_str}")

        # Add edges (connections between routers)
        for interface in router.get_interfaces():
            hosts = interface.get_other_hosts(router)

            if len(hosts) == 1:
                G.add_edge(router.name, hosts[0].name, label=str(interface.network))
            elif len(hosts) > 1:
                if f"{(str(interface.network))}" not in switches:
                    switches[f"{(str(interface.network))}"] = f"S{switches_count}"
                    G.add_node(f"{interface.network}", label=f"S{switches_count}\n{interface.network}")
                    G.add_edge(router.name, f"{interface.network}")
                    print(f"Added switch {interface.network}")
                    switches_count += 1
                else:
                    G.add_edge(router.name, f"{interface.network}")

    # Draw the graph with dynamic layout
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    node_labels = nx.get_node_attributes(G, 'label')

    plt.figure(figsize=(20, 10))  # Adjust the size of the figure
    plt.subplots_adjust(left=0.1, right=0.9)  # Add padding to the left and right of the image

    nx.draw_networkx_nodes(G, pos, node_color='cyan')
    nx.draw_networkx_edges(G, pos)

    # Manually add the labels using matplotlib's text function
    for node, (x, y) in pos.items():
        plt.text(x, y, node_labels[node], fontsize=6, color='black', weight='bold', ha='center', va='center')

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, rotate=False, verticalalignment='top',
                                 bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

    plt.axis('off')  # Disable axis
    if graph_file == "":
        graph_file = "network_map.pdf"
    else:
        graph_file = f"../../network_map_{graph_file}.pdf"
    plt.savefig(graph_file)  # Save as png


if __name__ == '__main__':
    network_manager = NetworkManager('10.0.0.2', 'rocom')
    draw_network_map(network_manager)

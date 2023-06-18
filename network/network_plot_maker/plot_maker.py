import networkx as nx
import matplotlib.pyplot as plt

from network.network_manager import NetworkManager


def draw_network_map(network_manager: NetworkManager):
    G = nx.Graph()

    # Add nodes (routers) to the graph
    for router in network_manager.routers:
        interfaces_str = "\n".join([str(interface) for interface in router.get_interfaces()])
        G.add_node(router.name, label=f"Name: {router.name}, Interfaces: \n{interfaces_str}")

        # Add edges (connections between routers)
        for interface in router.get_interfaces():
            for adjacent_router in interface.get_other_hosts(router):
                G.add_edge(router.name, adjacent_router.name, label=str(interface.network))  # Use the network as the label

    # Draw the graph with dynamic layout
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    node_labels = nx.get_node_attributes(G, 'label')

    plt.figure(figsize=(20, 10))  # Adjust the size of the figure
    plt.subplots_adjust(left=0.1, right=0.9)  # Add padding to the left and right of the image

    nx.draw_networkx_nodes(G, pos, node_color='blue')
    nx.draw_networkx_edges(G, pos)

    # Manually add the labels using matplotlib's text function
    for node, (x, y) in pos.items():
        plt.text(x, y, node_labels[node], fontsize=6, color='black', weight='bold', ha='center', va='center')

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, rotate=False, verticalalignment='top', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

    plt.axis('off')  # Disable axis
    plt.savefig("network_map.pdf")  # Save as png


if __name__ == '__main__':
    network_manager = NetworkManager('10.0.0.2', 'rocom')
    draw_network_map(network_manager)

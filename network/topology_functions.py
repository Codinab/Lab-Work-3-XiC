import networkx as nx
import matplotlib.pyplot as plt


def plot_network_topology(routers, connections):
    G = nx.Graph()

    for router in routers:
        G.add_node(router['sysname'])

    for connection in connections:
        G.add_edge(connection['source'], connection['destination'])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=8, font_weight='bold')
    plt.show()

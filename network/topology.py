import networkx as nx
import matplotlib.pyplot as plt


class NetworkTopology:
    def __init__(self):
        self.G = nx.Graph()

    def add_router(self, router):
        self.G.add_node(router)

    def add_connection(self, router1, router2):
        self.G.add_edge(router1, router2)

    def plot_topology(self):
        nx.draw(self.G, with_labels=True)
        plt.show()

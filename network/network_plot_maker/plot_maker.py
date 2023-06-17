import pygraphviz as pgv

from network.network_classes import Router
from network.network_manager import NetworkManager


class PlotMaker:
    def __init__(self):
        pass

    def generate_network_graph(self, routers):
        graph = pgv.AGraph(directed=True)

        for router in routers:
            graph.add_node(router.name, label=f"Router {router.name}")

            for interface in router.get_interfaces():
                graph.add_node(interface.name, label=f"Interface {interface.name}")

                graph.add_edge(router.name, interface.name,
                               label=f"{interface.ip.value} - {interface.speed} Mbps")

        graph.write("network.dot")
        graph.draw("network.pdf", prog="dot", format="pdf")

if __name__ == '__main__':
    network_manager = NetworkManager('10.0.0.2', 'rocom')
    pl_maker = PlotMaker()
    pl_maker.generate_network_graph(network_manager.routers)

class RouteSummarizer:
    def __init__(self, routing_table):
        self.routing_table = routing_table

    def create_route_summaries(self):
        route_summaries = []
        # Lògica de resum de ruta aquí
        # Aquest exemple és només un marcador de posició
        for destination, netmask in self.routing_table:
            summary = destination + "/" + netmask
            route_summaries.append(summary)
        return route_summaries

    @staticmethod
    def print_route_summaries(route_summaries):
        print("Route Summaries:")
        for summary in route_summaries:
            print(summary)

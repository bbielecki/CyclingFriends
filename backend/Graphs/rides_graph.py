import networkx as nx
from backend.Rides.DataAccess.rides_db_context import Session
from backend.Rides.Domain.clustered_rides import ClusteredRides


class RidesGraph:

    def __init__(self):
        self.nodes = []
        self.G = nx.Graph()

    def create_rides_graph(self, session):
        nodes = session.query(ClusteredRides)
        for n in nodes:
            self.G.add_edge(n.CluserId, n.RelatedClusterId, rideId=n.RideId)

        return self.G


def get_rides_graph():
    session = Session()
    rides_graph = RidesGraph()
    return rides_graph.create_rides_graph(session)

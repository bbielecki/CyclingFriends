import networkx as nx
from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.clustered_rides import ClusteredRides


class RidesGraph:

    def __init__(self):
        self.nodes = []
        self.G = nx.Graph()

    def create_rides_graph(self, session):
        nodes = session.query(ClusteredRides.ClusterId, ClusteredRides.RelatedClusterId, ClusteredRides.RideId, ClusteredRides.Id)
        for n in nodes:
            self.G.add_edge(n.ClusterId, n.RelatedClusterId, rideId=n.RideId, clusteredRideId=n.Id)

        return self.G


def get_rides_graph():
    session = Session()
    rides_graph = RidesGraph()
    return rides_graph.create_rides_graph(session)

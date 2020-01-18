import networkx as nx
from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.clustered_rides import ClusteredRides
from Rides.Domain.rides import Rides
from Rides.Domain.clusters import Clusters
from Rides.Domain.pois import Pois
from Users.Domain.user import User
from datetime import datetime


class RidesGraph:

    def __init__(self):
        self.nodes = []
        self.G = nx.Graph()

    def create_rides_graph(self, session):
        timestamp = datetime.now()

        nodes = session.query(ClusteredRides, Clusters, Pois, Rides, User)\
            .filter(ClusteredRides.ClusterId == Clusters.Id)\
            .filter(Clusters.Id == Pois.ClusterId)\
            .filter(ClusteredRides.RideId == Rides.Id)\
            .filter(Rides.PlayerId == User.Id)

        for n in nodes:
            self.G.add_edge(
                n.ClusteredRides.ClusterId,
                n.ClusteredRides.RelatedClusterId,
                rideId=n.ClusteredRides.RideId,
                clusteredRideId=n.ClusteredRides.Id,
                userId=n.User.Id,
                UserWeight=n.User.Weight,
                UserGender=n.User.Gender,
                UserHasGarmin=n.User.HasGarmin,
                tags=n.Pois.Tags
            )

        print("Graph creation time: ", datetime.now() - timestamp)
        print(self.G.number_of_nodes())
        print(self.G.number_of_edges())
        return self.G


def get_rides_graph():
    session = Session()
    rides_graph = RidesGraph()
    return rides_graph.create_rides_graph(session)

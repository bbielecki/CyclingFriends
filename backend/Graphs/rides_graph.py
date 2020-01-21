import networkx as nx
from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.clustered_rides import ClusteredRides
from Rides.Domain.rides import Rides
from Rides.Domain.clusters import Clusters
from Rides.Domain.pois import Pois
from Users.Domain.user import User
from datetime import datetime
from sqlalchemy.orm import aliased


class RidesGraph:

    def __init__(self):
        self.nodes = []
        self.G = nx.Graph()

    def create_rides_graph(self, session, limit: int = None):
        timestamp = datetime.now()

        nodes = self.get_nodes(session, limit)

        for n in nodes:
            # add ride start node
            if not self.G.has_node(n.ClusteredRides.ClusterId):
                self.G.add_node(n.ClusteredRides.ClusterId,
                                Type="poi",
                                clusteredRideId=n.ClusteredRides.Id,
                                tags=n[2].Tags)

            # add ride end node
            if not self.G.has_node(n.ClusteredRides.RelatedClusterId):
                self.G.add_node(n.ClusteredRides.RelatedClusterId,
                                Type="poi",
                                clusteredRideId=n.ClusteredRides.Id,
                                tags=n[3].Tags)

            # add ride edge
            if self.G.has_edge(n.ClusteredRides.ClusterId, n.ClusteredRides.RelatedClusterId):
                self.G[n.ClusteredRides.ClusterId][n.ClusteredRides.RelatedClusterId]['weight'] += 1
            else:
                self.G.add_edge(
                    n.ClusteredRides.ClusterId,
                    n.ClusteredRides.RelatedClusterId,
                    rideId=n.ClusteredRides.RideId,
                    clusteredRideId=n.ClusteredRides.Id,
                    userId=n.User.Id,
                    weight=1
                )

        print("Rides Graph creation time: ", datetime.now() - timestamp)
        print(self.G.number_of_nodes())
        print(self.G.number_of_edges())
        return self.G

    def get_nodes(self, session, limit: int = None):
        start_pois = aliased(Pois)
        end_pois = aliased(Pois)
        nodes = session.query(ClusteredRides, Clusters, start_pois, end_pois, Rides, User) \
            .filter(ClusteredRides.ClusterId == Clusters.Id) \
            .filter(ClusteredRides.ClusterId == start_pois.ClusterId) \
            .filter(ClusteredRides.RelatedClusterId == end_pois.ClusterId) \
            .filter(ClusteredRides.RideId == Rides.Id) \
            .filter(Rides.PlayerId == User.Id)

        if limit is not None:
            nodes = nodes.limit(limit)

        return nodes

    def create_bipartite_graph(self, session, limit: int = None):

        timestamp = datetime.now()

        nodes = self.get_nodes(session, limit)

        for n in nodes:
            # add user node
            if not self.G.has_node(n.User.Id):
                self.G.add_node(n.User.Id,
                                Type="user",
                                UserWeight=n.User.Weight,
                                UserGender=n.User.Gender,
                                UserHasGarmin=n.User.HasGarmin)

            # add ride start node
            if not self.G.has_node(n.ClusteredRides.ClusterId):
                self.G.add_node(n.ClusteredRides.ClusterId,
                                Type="poi",
                                clusteredRideId=n.ClusteredRides.Id,
                                tags=n[2].Tags)

            # add ride end node
            if not self.G.has_node(n.ClusteredRides.RelatedClusterId):
                self.G.add_node(n.ClusteredRides.RelatedClusterId,
                                Type="poi",
                                clusteredRideId=n.ClusteredRides.Id,
                                tags=n[3].Tags)

            # add ride edge
            if self.G.has_edge(n.ClusteredRides.ClusterId, n.ClusteredRides.RelatedClusterId):
                self.G[n.ClusteredRides.ClusterId][n.ClusteredRides.RelatedClusterId]['weight'] += 1
            else:
                self.G.add_edge(
                    n.ClusteredRides.ClusterId,
                    n.ClusteredRides.RelatedClusterId,
                    rideId=n.ClusteredRides.RideId,
                    clusteredRideId=n.ClusteredRides.Id,
                    userId=n.User.Id,
                    weight=1
                )

            # add user to pois edges
            if self.G.has_edge(n.User.Id, n.ClusteredRides.ClusterId):
                self.G[n.User.Id][n.ClusteredRides.ClusterId]['weight'] += 1
            else:
                self.G.add_edge(
                    n.User.Id,
                    n.ClusteredRides.ClusterId,
                    rideId=n.ClusteredRides.RideId,
                    clusteredRideId=n.ClusteredRides.Id,
                    userId=n.User.Id,
                    weight=1
                )
            if self.G.has_edge(n.User.Id, n.ClusteredRides.RelatedClusterId):
                self.G[n.User.Id][n.ClusteredRides.RelatedClusterId]['weight'] += 1
            else:
                self.G.add_edge(
                    n.User.Id,
                    n.ClusteredRides.RelatedClusterId,
                    rideId=n.ClusteredRides.RideId,
                    clusteredRideId=n.ClusteredRides.Id,
                    userId=n.User.Id,
                    weight=1
                )

        print("User & Rides bipartite Graph creation time: ",
              datetime.now() - timestamp)
        print("Number of nodes: {0}".format(self.G.number_of_nodes()))
        print("Number of edges: {0}".format(self.G.number_of_edges()))
        return self.G


def get_rides_graph(limit: int = None):
    session = Session()
    rides_graph = RidesGraph()
    return rides_graph.create_rides_graph(session, limit)


def get_users_and_rides_graph(limit: int = None):
    session = Session()
    rides_graph = RidesGraph()
    return rides_graph.create_bipartite_graph(session, limit)

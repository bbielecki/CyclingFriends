from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.pois import Pois
import Rides.clusters_qh as clusters
from osm.get_poi import get_poi
import json

session = Session()


def add_poi(poi: Pois):
    session.add(poi)
    session.commit()


def add_pois():
    clusterCenters = clusters.get_clusters_center()
    for cc in clusterCenters:
        poi = (get_poi(cc['centerLat'],
                       cc['centerLng'], 250, 1))
        if len(poi) > 0:
            new_poi = Pois(ClusterId=cc['ClusterId'],
                           Lat=poi[0].lat(), Lng=poi[0].lon(), Tags=json.dumps(poi[0].tags()))
            add_poi(new_poi)

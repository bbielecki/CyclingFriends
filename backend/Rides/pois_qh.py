from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.pois import Pois
import Rides.clusters_qh as clusters
from osm.get_poi import get_poi
import json

session = Session()


def add_poi(poi: Pois):
    session.add(poi)
    session.commit()


def add_pois(skip: int = None, limit: int = None):
    clusterCenters = clusters.get_clusters_center(skip, limit)
    for cc in clusterCenters:
        poi = (get_poi(cc['centerLat'],
                       cc['centerLng'], 250, 1))
        if len(poi) > 0:
            new_poi = Pois(ClusterId=cc['ClusterId'],
                           Lat=poi[0].lat(), Lng=poi[0].lon(), Tags=json.dumps(poi[0].tags()))
            add_poi(new_poi)


def get_pois(limit: int = None):
    pois = session.query(Pois.Id, Pois.ClusterId,
                         Pois.Lat, Pois.Lng, Pois.Tags)
    if limit is not None:
        pois = pois.limit(limit=limit)
    else:
        pois = pois.all()

    res = []
    for p in pois:
        poi = {
            'Id': p[0],
            'ClusterId': p[1],
            'Lat': p[2],
            'Lng': p[3],
            'Tags': p[4],
        }
        res.append(poi)
    return res

from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.clusters import Clusters

session = Session()


def get_clusters(skip: int = None, limit: int = None):
    clusters = session.query(Clusters.Id, Clusters.MinLat,
                             Clusters.MinLng, Clusters.MaxLat, Clusters.MaxLng).order_by(Clusters.Id)

    if limit is not None:
        clusters = clusters.limit(limit=limit)
    if skip is not None:
        clusters = clusters.offset(offset=skip)
    else:
        clusters = clusters.all()

    res = []
    for c in clusters:
        cluster = {
            'Id': c[0],
            'MinLat': c[1],
            'MinLng': c[2],
            'MaxLat': c[3],
            'MaxLng': c[4],
        }
        res.append(cluster)
    return res


def get_clusters_center(skip: int = None, limit: int = None):
    clusters = get_clusters(skip, limit)

    res = []
    for c in clusters:
        centerLat = (c['MaxLat'] - c['MinLat'])/2 + c['MinLat']
        centerLng = (c['MaxLng'] - c['MinLng'])/2 + c['MinLng']
        clusterCenter = {
            'ClusterId': c['Id'],
            'centerLat': centerLat,
            'centerLng': centerLng
        }
        res.append(clusterCenter)
    return res

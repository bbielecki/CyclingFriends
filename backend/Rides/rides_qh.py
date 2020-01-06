from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.rides import Rides

session = Session()


def get_rides():
    rides = session.query(Rides.Id, Rides.StartLocation_Latitude, Rides.StartLocation_Longitude, Rides.EndLocation_Latitude, Rides.EndLocation_Longitude).limit(limit=100)
    res = []
    for a in rides:
        res.append((a[0], a[1], a[2]))
        res.append((a[0], a[3], a[4]))
    return res
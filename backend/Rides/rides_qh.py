from backend.Rides.DataAccess.rides_db_context import Session
from backend.Rides.Domain.rides import Rides

session = Session()


def get_rides():
    rides = session.query(Rides.Id, Rides.StartLocation_Latitude, Rides.StartLocation_Longitude, Rides.EndLocation_Latitude, Rides.EndLocation_Longitude).limit(limit=100)
    res = []
    for r in rides:
        ride = {
            'Id': r[0],
            'StartLocation_Latitude': r[1],
            'StartLocation_Longitude': r[2],
            'EndLocation_Latitude': r[3],
            'EndLocation_Longitude': r[4],
        }
        res.append(ride)
    return res
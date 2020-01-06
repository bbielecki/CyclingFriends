from Rides.DataAccess.rides_db_context import Session
from Rides.Domain.rides import Rides

session = Session()


def get_rides():
    return session.query(Rides.Id, Rides.StartLocation_Latitude, Rides.StartLocation_Longitude, Rides.EndLocation_Latitude, Rides.EndLocation_Longitude).first()

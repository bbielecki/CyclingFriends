from sqlalchemy import Table, Column, ForeignKey, Integer, Float, String, Binary, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, relation
from Rides.Domain.rides import Rides

Base = declarative_base(metadata=MetaData(schema='rides'))


class ClusteredRides(Base):
    __tablename__ = "ClusteredRides"

    Id = Column(String, primary_key=True)
    ClusterId = Column(Integer)
    RelatedClusterId = Column(Integer)
    RideId = Column(String)
    Lat = Column(Float)
    Lng = Column(Float)
    Start = Column(Binary)

    # Ride = relation(Rides, backref='ClusteredRides')

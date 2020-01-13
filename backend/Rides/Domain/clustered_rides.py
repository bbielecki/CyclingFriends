from sqlalchemy import Column, Integer, Float, String, Binary, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='rides'))


class ClusteredRides(Base):
    __tablename__ = "ClusteredRides"

    Id = Column(String, primary_key=True)
    ClusterId = Column(Integer)
    RideId = Column(String)
    Lat = Column(Float)
    Lng = Column(Float)
    Start = Column(Binary)

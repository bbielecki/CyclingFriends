from sqlalchemy import Column, ForeignKey, Integer, Float, String, Binary, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema='rides'))


class ClusteredRides(Base):
    __tablename__ = "ClusteredRides"

    Id = Column(String, primary_key=True)
    ClusterId = Column(Integer)
    RelatedClusterId = Column(Integer)
    RideId = Column(String, ForeignKey("ARides.Id"))
    Lat = Column(Float)
    Lng = Column(Float)
    Start = Column(Binary)

    Ride = relationship("Rides", foreign_key=[RideId])

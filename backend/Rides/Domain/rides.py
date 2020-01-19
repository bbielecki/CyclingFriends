from sqlalchemy import Column, ForeignKey, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema='rides'))


class Rides(Base):
    __tablename__ = "ARides"

    Id = Column(String, primary_key=True)
    PlayerId = Column(String)
    StartLocation_Longitude = Column(Float)
    StartLocation_Latitude = Column(Float)
    EndLocation_Longitude = Column(Float)
    EndLocation_Latitude = Column(Float)

    # Players = relationship("Player", foreign_keys=[PlayerId])

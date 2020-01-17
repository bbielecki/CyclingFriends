from sqlalchemy import Column, ForeignKey, String, Float, MetaData, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='rides'))


class Pois(Base):
    __tablename__ = "Pois"

    Id = Column(Integer, primary_key=True)
    ClusterId = Column(Integer)
    Lat = Column(Float)
    Lng = Column(Float)
    Tags = Column(String)

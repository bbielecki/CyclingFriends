from sqlalchemy import Column, Integer, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='rides'))


class Clusters(Base):
    __tablename__ = "Clusters"

    Id = Column(Integer, primary_key=True)
    MinLat = Column(Float)
    MinLng = Column(Float)
    MaxLat = Column(Float)
    MaxLng = Column(Float)

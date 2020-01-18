from sqlalchemy import Column, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='rides'))


class Player(Base):
    __tablename__ = "APlayers"

    Id = Column(String, primary_key=True)
    Weight = Column(Float)
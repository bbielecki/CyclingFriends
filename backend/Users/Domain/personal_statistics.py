from sqlalchemy import Column, Integer, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='players'))


class PersonalStatistics(Base):
    __tablename__ = "APersonalStatistics"

    Id = Column(String, primary_key=True)
    TotalRides = Column(Integer)
    TotalDistance = Column(Float)
    TotalCalories = Column(Float)
    TotalSavedCO2 = Column(Float)
    Level = Column(Integer)
    LevelPoints = Column(Integer)
    TotalBonusRides = Column(Integer)

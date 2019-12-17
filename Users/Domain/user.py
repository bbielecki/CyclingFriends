from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'players.AUsers'

    Id = Column(String, primary_key=True)
    Weight = Column(Integer)
    DateCreated = Column(DateTime)
    City = Column(String)
    DateOfBirth = Column(DateTime)
    UserType = Column(Integer)
    UserBadges = relationship("AUserBadges", schema="players", back_populates="AUsers")
    PersonalStatistics = relationship("APersonalStatistics", schema="players", back_populates="AUsers")

    def __repr__(self):
        return "<User(Id='%s', Wight='%s', DateOfBirth='%s', City='%s'>" \
               % (self.Id, self.Weight, self.DateOfBirth, self.City)
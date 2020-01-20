from sqlalchemy import Column, Integer, String, DateTime, MetaData, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema='players'))


class User(Base):
    __tablename__ = 'AUsers'

    Id = Column(String, primary_key=True)
    Weight = Column(Integer)
    DateCreated = Column(DateTime)
    City = Column(String)
    DateOfBirth = Column(DateTime)
    UserType = Column(Integer)
    Gender = Column(Integer)
    HasGarmin = Column(Boolean)
    # UserBadges = relationship("AUserBadges", back_populates="AUsers")

    def __repr__(self):
        return "<User(Id='%s', Wight='%s', DateOfBirth='%s', City='%s'>" \
               % (self.Id, self.Weight, self.DateOfBirth, self.City)
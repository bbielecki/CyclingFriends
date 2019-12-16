from sqlalchemy import Column, Integer, String, DateTime

class User():
    __tablename__ = 'players.AUsers'

    Id = Column(String, primary_key=True)
    Weight = Column(Integer)
    DateCreated = Column(DateTime)
    City = Column(String)
    DateOfBirth = Column(DateTime)
    UserType = Column(Integer)

    def __repr__(self):
        return "<User(Id='%s', Wight='%s', DateOfBirth='%s', City='%s'>" \
               % (self.Id, self.Weight, self.DateOfBirth, self.City)

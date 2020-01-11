from Users.DataAccess.users_db_context import Session
from Users.Domain.user import User

session = Session()


def get_users():
    for city, weight, id in session.query(User.City, User.Weight, User.Id).limit(limit=10):
        print(city, weight, id)

from backend.Users.DataAccess.users_db_context import Session
from backend.Users.Domain.personal_statistics import PersonalStatistics

session = Session()


def get_stats():
    for lvl, pts in session.query(PersonalStatistics.Level, PersonalStatistics.TotalDistance).limit(limit=5):
        print(lvl, pts)

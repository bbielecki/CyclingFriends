import Services.db_connection as connection

db = connection.db
engine = connection.engine
metadata = db.MetaData(bind=engine)
users = db.Table('AUsers', metadata, schema="players",  autoload=True, autoload_with=engine)
personal_statistics = db.Table('APersonalStatistics', metadata, schema="players",  autoload=True, autoload_with=engine)
daily_statistics = db.Table('ADailyStatistics', metadata, schema="players",  autoload=True, autoload_with=engine)
user_badges = db.Table('AUserBadges', metadata, schema="players",  autoload=True, autoload_with=engine)
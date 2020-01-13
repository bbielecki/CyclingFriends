import backend.Services.db_connection as connection
from sqlalchemy.orm import sessionmaker

db = connection.db
engine = connection.engine
metadata = db.MetaData(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)

players = db.Table('APlayers', metadata, schema="rides",
                   autoload=True, autoload_with=engine)
player_rides = db.Table('APlayerRide', metadata,
                        schema="rides",  autoload=True, autoload_with=engine)
rides = db.Table('ARides', metadata, schema="rides",
                 autoload=True, autoload_with=engine)
strava_athletes = db.Table('AStravaAthletes', metadata,
                           schema="rides",  autoload=True, autoload_with=engine)
garmin_athletes = db.Table('AGarminAthletes', metadata,
                           schema="rides",  autoload=True, autoload_with=engine)

import backend.configuration as cfg
import sqlalchemy as db
from urllib.parse import quote_plus

params = cfg.db_config['connection_string']
engine = db.create_engine('mssql+pyodbc://%s' % params)
connection = engine.connect()



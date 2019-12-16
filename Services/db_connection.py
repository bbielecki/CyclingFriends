import configuration as cfg
import sqlalchemy as sa
from urllib.parse import quote_plus

params = quote_plus(cfg.db_config['connection_string'])
engine = sa.create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)




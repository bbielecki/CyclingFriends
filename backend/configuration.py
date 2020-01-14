import os
from dotenv import load_dotenv
load_dotenv()

db_config = {'connection_string': os.getenv("CONNECTION_STRING")}

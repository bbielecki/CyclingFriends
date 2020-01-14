from dotenv import load_dotenv
load_dotenv()
import os
# windows
print(os.getenv("CONNECTION_STRING"))
db_config = {'connection_string': os.getenv("CONNECTION_STRING")}

# linux
# db_config = {'connection_string': 'sa:Passw12#@127.0.0.1/activy_anonimized?driver=ODBC+Driver+17+for+SQL+Server'}

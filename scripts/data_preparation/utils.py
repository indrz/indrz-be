
import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
ogr_db_con = f"PG: host={db_host} user={db_user} dbname={db_name} password={db_pass}"

unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO', 'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']


import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"


db_dj_user = os.getenv('DB_DJ_USER')
db_dj_name = os.getenv('DB_DJ_NAME')
db_dj_host = os.getenv('DB_DJ_HOST')
db_dj_pass = os.getenv('DB_DJ_PASSWORD')
db_dj_port = os.getenv('DB_DJ_PORT')

con_dj_string = f"dbname={db_dj_name} user={db_dj_user} host={db_dj_host} password={db_dj_pass}"

ogr_db_con = f"PG: host={db_host} user={db_user} dbname={db_name} password={db_pass}"

unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO', 'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']


def get_floor_float(name):
    """
    assuming input name is like "DA_EG_03_2019.dxf"
    :param name: dxf file name like "DA_EG_03_2019.dxf"
    :return: float value of floor
    """

    floor_names_odd = ['ZD', 'ZE', 'ZU', 'DG', 'EG', 'SO']
    floor_names_u = ['U1', 'U2', 'U3', 'U4']
    floor_names_z = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']
    floor_names_int = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    if not name:
        return name
    # floor = name.split("_")[-3]

    floor = name

    if floor in floor_names_odd:
        if floor == "EG":
            floor = 0.0
        elif floor == "SO":
            floor = -0.5
        elif floor == "ZE":
            floor = 0.5
        elif floor == "ZU":
            floor = -1.5
        else:
            floor = 9999.0
    elif floor in floor_names_z:
        # zwischen stock
        floor = float(floor[1])*1.0 + 0.5

    elif floor in floor_names_int:
        floor = float(floor)*1.0

    elif floor in floor_names_u:
        # underground
        floor = float(floor[1]) * -1.0
    else:
        floor = 9999.0


    return floor*1.0

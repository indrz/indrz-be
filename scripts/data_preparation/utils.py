import os
from dotenv import load_dotenv
load_dotenv()

# db_user = os.getenv('DB_USER')
# db_name = os.getenv('DB_NAME')
# db_host = os.getenv('DB_HOST')
# db_pass = os.getenv('DB_PASSWORD')
# db_port = os.getenv('DB_PORT')

db_user_navigatur = os.getenv('POSTGRES_USER_LIVE')
db_name_navigatur = os.getenv('POSTGRES_DB_LIVE')
db_host_navigatur = os.getenv('POSTGRES_HOST_LIVE')
db_pass_navigatur = os.getenv('POSTGRES_PASS_LIVE')
db_port_navigatur = os.getenv('POSTGRES_PORT_LIVE')

db_user_local = os.getenv('POSTGRES_USER_LOCALHOST')
db_name_local = os.getenv('POSTGRES_DB_LOCALHOST')
db_host_local = os.getenv('POSTGRES_HOST_LOCALHOST')
db_pass_local = os.getenv('POSTGRES_PASS_LOCALHOST')
db_port_local = os.getenv('POSTGRES_PORT_LOCALHOST')

# db_user = os.getenv('DB_DJ_USER')
# db_name = os.getenv('DB_DJ_NAME')
# db_host = os.getenv('DB_DJ_HOST')
# db_pass = os.getenv('DB_DJ_PASSWORD')
# db_port = os.getenv('DB_DJ_PORT')

db_dj_user = os.getenv('POSTGRES_USER')
db_dj_name = os.getenv('POSTGRES_DB')
db_dj_host = os.getenv('POSTGRES_HOST')
db_dj_pass = os.getenv('POSTGRES_PASS')
db_dj_port = os.getenv('POSTGRES_PORT')

db_tuindrz_user = os.getenv('POSTGRES_USER_INDRZ')
db_tuindrz_name = os.getenv('POSTGRES_DB_INDRZ')
db_tuindrz_host = os.getenv('POSTGRES_HOST_INDRZ')
db_tuindrz_pass = os.getenv('POSTGRES_PASS_INDRZ')
db_tuindrz_port = os.getenv('POSTGRES_PORT_INDRZ')

con_string_navigatur = f"dbname={db_name_navigatur} user={db_user_navigatur} host={db_host_navigatur} password={db_pass_navigatur} port={db_port_navigatur}"
# con_string_indrzlive = f"dbname={db_name} user={db_user} host={db_host} password={db_pass} port={db_port}"
con_string_localhost = f"dbname={db_name_local} user={db_user_local} host={db_host_local} password={db_pass_local} port={db_port_local}"
con_dj_string = f"dbname={db_dj_name} user={db_dj_user} host={db_dj_host} password={db_dj_pass} port={db_dj_port}"
ogr_db_con = f"PG: host={db_host_local} user={db_user_local} dbname={db_name_local} password={db_pass_local} port={db_port_local}"
con_tuindrz = f"dbname={db_tuindrz_name} user={db_tuindrz_user} host={db_tuindrz_host} password={db_tuindrz_pass} port={db_tuindrz_port}"


unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO', 'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']
unique_floor_map = [{'name': '01', 'number': 1.0}, {'name': '02', 'number': 2.0}, {'name': '03', 'number': 3.0},
                      {'name': '04', 'number': 4.0}, {'name': '05', 'number': 5.0}, {'name': '06', 'number': 6.0},
                      {'name': '07', 'number': 7.0}, {'name': '08', 'number': 8.0}, {'name': '09', 'number': 9.0},
                      {'name': '10', 'number': 10.0}, {'name': '11', 'number': 11.0}, {'name': '12', 'number': 12.0},
                      {'name': 'DG', 'number': 9999}, {'name': 'EG', 'number': 0.0}, {'name': 'SO', 'number': -0.5},
                      {'name': 'U1', 'number': -1.0}, {'name': 'U2', 'number': -2.0}, {'name': 'U3', 'number': -3.0},
                      {'name': 'U4', 'number': -4.0}, {'name': 'Z1', 'number': 1.5}, {'name': 'Z2', 'number': 2.5},
                      {'name': 'Z3', 'number': 3.5}, {'name': 'Z4', 'number': 4.5}, {'name': 'Z5', 'number': 5.5},
                      {'name': 'ZD', 'number': 9999}, {'name': 'ZE', 'number': 0.5}, {'name': 'ZU', 'number': -0.5}]


# TRAKTS
#Karlsplatz ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AP', 'AQ', 'AS', 'AT', 'EA', 'EB', 'EC']
#Getreidemarkt ['BA', 'BB', 'BC', 'BD', 'BE', 'BG', 'BH', 'BI', 'BK', 'BL', 'BZ', 'PF', 'QA']
#Gusshaus ['CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'FA', 'FB', 'FC', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HK', 'HL']
#Freihaus ['DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'ZA', 'ZB', 'ZC', 'ZD']
#Arsenal ['MA', 'MB', 'MC', 'MD', 'MG', 'MH', 'MI', 'OA', 'OB', 'OC', 'OY', 'OZ']
#Ausweichquartier ['WA', 'WB', 'WC', 'WD']

def floor_map():
    unique_floor_name_map = []
    for f in unique_floor_names:
        value = ""
        if f == "DG":
            value = "Dachgeschoß"
        elif f == "EG":
            value = "Erdgeschoß"
        elif f == "SO":
            value = "Souterrain"
        elif f.startswith("U"):
            value = "Untergeschoß"
        elif f.startswith("Z"):
            value = "Zwischengeschoß"
        else:
            value = "Obergeschoß"

        d = dict(value, f)
        unique_floor_name_map.append(d)

    return floor_map


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

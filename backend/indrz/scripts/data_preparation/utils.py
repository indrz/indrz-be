import os
import pathlib
from pathlib import Path, PurePath
curdir = os.path.dirname(os.path.abspath(__file__))

db_user = os.getenv('PG_USER')
db_name = os.getenv('PG_DB')
db_host = os.getenv('PG_HOST')
db_pass = os.getenv('PG_PASS')
db_port = os.getenv('PG_PORT')
GEOSERVER_USER = os.getenv('GEOSERVER_USER')
GEOSERVER_PASS = os.getenv('GEOSERVER_PASS')

dxf_root_path = os.getenv('DXF_ROOT_PATH')

con_dj_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass} port={db_port}"
ogr_db_con = f"PG: host={db_host} user={db_user} dbname={db_name} password={db_pass} port={db_port}"


unique_floor_numbers = ['0', '1', '2', '3']
unique_floor_names = ['eg', 'og01', 'og02', 'og03', 'og05']

# reassign all floors with ZD the floor number 10000

unique_floor_map = [{'name': '0_0', 'number': 0.0, 'vis_name': 'EG'},
                    {'name': '1_0', 'number': 1.0, 'vis_name': 'OG01'},
                    {'name': '2_0', 'number': 2.0, 'vis_name': 'OG02'},
                    {'name': '3_0', 'number': 3.0, 'vis_name': 'OG03'},
                    {'name': '5_0', 'number': 5.0, 'vis_name': 'OG05'}
                    ]


campus_names = ["Main AAU", "Lakeside", "Robert Musil Institut Bahnhofstraße", "IFF-Klagenfurt Sterneckstraße", "Sterneckstrasse" ]



color_ids = [
    {'type_id': 6, 'hexcolor': '#006BAC', 'name': 'Semin, Proj, Hörsaal'},
    {'type_id': 50, 'hexcolor': '#8AD1F5', 'name': 'Labor Buero'},
    {'type_id': 103, 'hexcolor': '#41A1DA', 'name': 'Sekretariat'},
    {'type_id': 63, 'hexcolor': '#99FFCC', 'name': 'Veranstaltung, turkis'},
    {'type_id': 65, 'hexcolor': '#008392', 'name': 'tuerkis'},
    {'type_id': 64, 'hexcolor': '#CCCCFF', 'name': 'Lernplatz'},
    {'type_id': 20, 'hexcolor': '#F5D0A8', 'name': 'Aula'},
    {'type_id': 109, 'hexcolor': '#42A12B', 'name': 'green'},
    {'type_id': 91, 'hexcolor': '#9D9D9D', 'name': 'wc'},
    {'type_id': 44, 'hexcolor': '#FFFFFF', 'name': 'white Stiegen, gang, lift'},
    {'type_id': 89, 'hexcolor': '#555555', 'name': 'wall cavity'},
    {'type_id': 94, 'hexcolor': '#9D9D9D', 'name': 'other'},
    {'type_id': 93, 'hexcolor': '#9D9D9D', 'name': 'other space type'}
]



def floor_float_to_string(floor_float):
    floor_name_geoserver = str(floor_float).replace('.', '_').replace('-', 'u')
    return floor_name_geoserver

def create_unique_floor_map():
    """
    create geoserver view names and db view names based on floor float value
    float 0.0 is then 0_0
    float -1.5 is then u1_5
    This is because geoserver cannot process names with .  like spaces_0.0 does not work
    Postgres also does not like names with .  so spaces_0_0 is ok
    """
    floor_list = []
    for floor in unique_floor_names:
        floor_float = get_floor_float(floor.upper())
        floor_string = str(floor_float)
        floor_string = floor_string.replace('.','_').replace('-','u')
        floor_json = {"name": floor_string, "number": floor_float}
        floor_list.append(floor_json)

    print(floor_list)


def get_floor_name(room_n, room_c, room_v):

    floor_name = ""
    trak_code = ""

    if room_n:
        if type(room_n) is str:
            # print("ROOM NUMBER IS ", room_n, floor_name)indrz_lines_03
            if len(room_n.split(' ')) == 3 :
                if room_n.split(' ')[1] in unique_floor_names:
                    floor_name = room_n.split(' ')[1]
                    trak_code = room_n.split(' ')[0]
    if room_c:
        if type(room_c) is str:
            if len(room_c.split(' ')) == 3 :
                if room_c.split(' ')[1] in unique_floor_names:
                    floor_name = room_c.split(' ')[1]
                    trak_code = room_c.split(' ')[0]
    if room_v:
        if type(room_v) is str:
            if len(room_v.split(' ')) == 3 :
                if room_v.split(' ')[1] in unique_floor_names:
                    floor_name = room_v.split(' ')[1]
                    trak_code = room_v.split(' ')[0]

    return floor_name, trak_code

def extract_building_code_names(filename):
    """
    TU has wings that either split a floor or map to an entire floor
    possible file names # 'OD_01_bp_052020'  or  BC_BG_U1_IP_042019
    :param filename: dxf filename with building codes
    :return:
    """
    list_floors = filename.split('_')
    building_code_list = list_floors[:-3]
    print("building code list ", building_code_list)
    if len(list_floors) > 3:
        # so more than one building code in filename
        pass
    print(list_floors)

    return building_code_list


def floor_map():
    unique_floor_name_map = []
    for f in unique_floor_names:
        value = ""
        if f == "DG" or f == "DACH":
            value = "Dachgeschoß"
        elif f == "EG":
            value = "Erdgeschoß"
        elif f == "SO":
            value = "Souterrain"
        elif f == "SOU":
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
    z_floor_exceptions = ['ZD', 'ZE', 'ZU', 'ZG', 'OG']
    floor_names_odd = ['UG', 'DG', 'EG', 'SO', 'SOU', 'DACH']

    if not name:
        return name
    # floor = name.split("_")[-3]

    floor = name.upper()

    if floor.startswith("D"):
        if floor == "DG" or floor == "DACH" or floor == "DG01":
            floor = 10001.0
        elif floor == "DG02":
            floor = 10002.0
        elif floor == "DG03":
            floor = 10003.0
        elif floor == "DG04":
            floor = 10004.0
    elif floor in floor_names_odd:
        if floor == "EG":
            floor = 0.0
        elif floor == "UG":
            floor = -1.0
        elif floor == "SO":
            floor = -0.5
        elif floor == "SOU":
            floor = -0.5
    elif floor in z_floor_exceptions:
        if floor == "ZE":
            floor = 0.5
        elif floor == "OG":
            floor = 1
        elif floor == "ZG":
            floor = 0.5
        elif floor == "ZU":
            floor = -1.5
        elif floor == "ZD":
            floor = 7777
    elif floor.startswith("OG"):
        floor = float(floor.upper()[2:])*1.0
    elif floor.startswith("Z") and floor not in z_floor_exceptions:
        # zwischen stock
        floor = float(floor[1])*1.0 + 0.5
    elif floor.startswith("U") and floor != "UG":
        # underground
        floor = float(floor[2:]) * -1.0
    else:
        floor = 4444.0

    return floor*1.0


def get_dxf_fullpath(dxf_file_name):
    dxf_dir_path = Path(os.getenv('DXF_ROOT_PATH') )
    if os.getenv('PROD') == '0':
        dxf_dir_path = Path(os.getenv('DXF_ROOT_PATH'))
    dxf_file_full_path = Path.joinpath(dxf_dir_path, dxf_file_name)
    return dxf_file_full_path


def get_dxf_files(campus_name="", filename_filter=None, only_dxf_names=False):
    """
    filename_filter:  only process files including these characters
       example filename_filter='A1_OG02'  will only import files
       that include A1_OG02 in the filename
    """
    # dxf_dir_path = Path(os.getenv('DXF_ROOT_PATH'))

    dxf_file_paths = []
    dxf_files = []
    for root, subdirs, files in os.walk(os.getenv('DXF_ROOT_PATH')):
        for name in files:
            dxf_file_full_path = os.path.join(root, name)
            if PurePath(name).suffix == ".dxf":
                if filename_filter:
                    # only process files that include filename_filter
                    if PurePath(name).name.startswith(filename_filter):
                        dxf_files.append(name)
                        dxf_file_paths.append(dxf_file_full_path)
                else:
                    # run for all .dxf files regardless of name
                    dxf_files.append(name)
                    dxf_file_paths.append(dxf_file_full_path)

    if only_dxf_names:
        return dxf_files
    else:
        return dxf_file_paths


def is_roomcode(value):
    if value:
        if type(value) is str:
            # print("ROOM NUMBER IS ", room_n, floor_name)indrz_lines_03
            if len(value.split(' ')) == 3 :
                if value.split(' ')[1] in unique_floor_names:
                    floor_name = value.split(' ')[1]
                    trak_code = value.split(' ')[0]
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def get_floor_str(floor_name_from_dwg_filename):
    """
    Inside the DWG plans the unique room codes are formed with a
    shorter floor name than the one used in the file name
    this function converts the floor name found in the filename
    into the same value found in the dwg block roomcode text
    """

    f_code = None
    f_float = get_floor_float(floor_name_from_dwg_filename)

    if f_float < 0:
        f_code = "U" + str(int(f_float) * -1)

    if f_float == 0:
        f_code = "EG"

    if f_float > 0 and f_float < 10000:
        f_code = "0" + str(int(f_float))

    if f_float > 10000:
        f_code = "D" + str(int(f_float - 10000))

    if f_float == 0.5:
        f_code = "ZE"
    return f_code



def generate_unique_roomcode(all_floors, dbschema='pre_django'):
    # delete ALL labels for ENTIRE CAMPUS

    del_sql = f"""delete from {dbschema}.{table_name} l where l.id in
                       (select l.id from pre_django.{table_name} l, 
                       django.buildings_campus c
                        where ST_CoveredBy(st_transform(l.geom, 3857), c.geom)
                        AND c.campus_name = '{campus}')"""
    cur.execute(del_sql)
    for floor in all_floors:
        types = ['labels', 'lines', 'spaces', 'umriss']
        for type in types:
            table_name = f"indrz_{type}_{floor}"
            del_sql = f"""delete from {dbschema}.{table_name} l where l.id in
                               (select l.id from pre_django.{table_name} l, 
                               django.buildings_campus c
                                where ST_CoveredBy(st_transform(l.geom, 3857), c.geom)
                                AND c.campus_name = '{campus}')"""
            cur.execute(del_sql)
            conn.commit()

if __name__ == '__main__':

    path = "/mnt/c/Users/mdiener/GOMOGI/BOKU-indrz - Documents/03_Working-Data/dwg/"
    unique_floors = []
    unique_buildings = []
    for root, subdirs, files in os.walk(path):
        for name in files:
            # print(os.path.join(path, name))
            filepath = pathlib.PurePath(root, name)
            fullpath = os.path.join(root, name)
            print(fullpath)
            foldername = str(filepath.parent).split('\\')[-1]
            filename = filepath.name
            floor = str(filepath.stem).split('_')[-1]
            building = str(filepath.stem).split('_')[0]
            if filepath.suffix == '.dwg':
                if floor not in unique_floors:
                    unique_floors.append(floor)
                if building not in unique_buildings:
                    unique_buildings.append(building)

    print("floors ", unique_floors)
    print("buildings ", unique_buildings)

    for floor_name in unique_floors:
        floor_float = get_floor_float(floor_name)
        floor_str = get_floor_str(floor_name)
        print(floor_name, floor_float, " fcode ", floor_str)
    for building in unique_buildings:
        print(building)
    #
    # print(get_dxf_files("foor", only_dxf_names=True))

    # floor_float_to_string()

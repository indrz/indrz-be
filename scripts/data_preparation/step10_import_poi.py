import psycopg2
from utils import con_string_navigatur, get_floor_float, unique_floor_names, con_dj_string


conn = psycopg2.connect(con_string_navigatur)
cur = conn.cursor()

def create_poi_wings():
    """
    We created all wings as points only for the EG
    using this data we auto generate points for
    all other floors with correct wing names
    """

    ftraks = [{'floor': '01', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AP', 'AQ', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HL', 'MG', 'MH', 'OA', 'OB', 'OC', 'OY', 'OZ', 'QA', 'ZA', 'ZB', 'ZC']}, {'floor': '02', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AP', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'OA', 'OB', 'OY', 'OZ', 'QA', 'WA', 'WB', 'WC', 'WD']}, {'floor': '03', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HK', 'OB', 'OY', 'OZ', 'WB', 'WC', 'WD']}, {'floor': '04', 'traks': ['AA', 'AB', 'AC', 'AD', 'AK', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'FB', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HK', 'HL']}, {'floor': '05', 'traks': ['BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'CA', 'CB', 'CD', 'CG', 'DA', 'DB', 'DC', 'DD', 'DF', 'EA', 'FB', 'HA', 'HB', 'HC', 'HD', 'HF', 'HG']}, {'floor': '06', 'traks': ['BA', 'BB', 'BD', 'BE', 'BI', 'CA', 'CB', 'CD', 'CG', 'DA', 'DB', 'DC', 'DD', 'DF']}, {'floor': '07', 'traks': ['BA', 'BD', 'BI', 'DA', 'DB', 'DC', 'DD', 'GA']}, {'floor': '08', 'traks': ['BA', 'BI', 'DA', 'DB', 'DC']}, {'floor': '09', 'traks': ['BA', 'BI', 'DA', 'DB']}, {'floor': '10', 'traks': ['BA', 'BI', 'DB']}, {'floor': '11', 'traks': ['BA', 'DB']}, {'floor': '12', 'traks': ['DB']}, {'floor': 'DG', 'traks': ['AB', 'AC', 'AF', 'AG', 'BA', 'BD', 'BE', 'BI', 'BZ', 'CF', 'CG', 'CI', 'DD', 'DE', 'EA', 'EB', 'EC', 'GA', 'ZA', 'ZB', 'ZC']}, {'floor': 'EG', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AP', 'AQ', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'FC', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HK', 'MA', 'MB', 'MC', 'MD', 'MG', 'MH', 'MI', 'OA', 'OB', 'OC', 'OY', 'OZ', 'PF', 'QA', 'WA', 'WB', 'WD', 'ZA', 'ZB', 'ZC', 'ZD']}, {'floor': 'SO', 'traks': ['CF']}, {'floor': 'U1', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AI', 'AK', 'AP', 'AQ', 'AS', 'BA', 'BB', 'BC', 'BD', 'BE', 'BG', 'BH', 'BI', 'BK', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'FC', 'GA', 'MD', 'OA', 'OB', 'OC', 'OY', 'OZ', 'QA', 'WA', 'WB', 'WC', 'WD', 'ZA', 'ZB', 'ZC', 'ZD']}, {'floor': 'U2', 'traks': ['AE', 'BA', 'BC', 'BD', 'BG', 'BI', 'BK', 'BL', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'DA', 'DB', 'DC', 'DD', 'DE', 'EB', 'GA', 'OY', 'OZ', 'WA', 'ZA', 'ZB']}, {'floor': 'U3', 'traks': ['DA', 'DB', 'DC', 'DD', 'DE']}, {'floor': 'U4', 'traks': ['DA', 'DB', 'DC']}, {'floor': 'Z1', 'traks': ['AA', 'AC', 'AE']}, {'floor': 'Z2', 'traks': ['AC', 'AF', 'AG', 'CF']}, {'floor': 'Z3', 'traks': ['AA', 'AC', 'AE']}, {'floor': 'Z4', 'traks': ['AC', 'BB']}, {'floor': 'Z5', 'traks': ['BB']}, {'floor': 'ZD', 'traks': ['AF']}, {'floor': 'ZE', 'traks': ['AA', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AK', 'CD', 'DE', 'EA', 'FA', 'FB', 'FC', 'OC', 'QA']}, {'floor': 'ZU', 'traks': ['AE', 'AP', 'BA', 'ZD']}]

    for floor in ftraks:

        if floor['floor'] in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "EG", "12", "Z5", "SO", "ZD"]:
            continue
        else:
            floor_name = floor['floor']
            traks = floor['traks']
            t2 = tuple(traks)

            floor_float = get_floor_float(floor_name)

            sql = f"""INSERT INTO django.poi_manager_poi (name, description, floor_num, floor_name, campus_id, 
                        category_id, geom)
                SELECT name, description, {floor_float}, '{floor_name}', campus_id, 80, geom  
                FROM django.poi_manager_poi 
                WHERE upper(name) in {t2}
                AND floor_name = 'EG' ;"""

            print(sql)

            cur.execute(sql)
            res = conn.commit()


def create_poi():

    key_names = [{'name':'STIEG', 'cat-id':33}, {'name': 'MENS', 'cat-id':33}, {'name': 'WC', 'cat-id':53},
                 {'name':'LIFT', 'cat-id':33}, {'name':'SEMIN', 'cat-id':33}, {'name':'LABO', 'cat-id':33},
                 {'name':'BIBL', 'cat-id':33},{'name': 'SEK', 'cat-id':33}, {'name':'FEST', 'cat-id':33},
                 {'name':'DEKAN', 'cat-id':33}, {'name':'HILF', 'cat-id':33}, {'name':'FEUER', 'cat-id':33},
                 {'name':'SAMMEL','cat-id':33}]

    for search_text in key_names:

        name = search_text['name']
        cat_id = search_text['cat-id']

        print(f"now running {search_text}")

        for floor_name in unique_floor_names:

            floor_float = get_floor_float(floor_name)

            sel_space = f"""INSERT INTO django.poi_manager_poi (name, description, floor_num, fk_campus_id, category_id, geom)
                SELECT room_description, room_code, {floor_float}, 1, {cat_id}, ST_Multi(ST_PointOnSurface(ST_Transform(geom, 3857))) 
                FROM campuses.indrz_spaces_{floor_name.lower()} 
                WHERE upper(room_description) like '%{name.upper()}%'
                AND st_isvalid(geom);"""

            cur.execute(sel_space)
            res = conn.commit()


def update_space_type_id():

    # assign all spaces a default value of 94
    # this enables geoserver to at least render roomcodes correctly
    ss = "update django.buildings_buildingfloorspace set space_type_id = 94 where space_type_id ISNULL"
    cur.execute(ss)
    conn.commit()


    search_text_list = ['STIEG', 'MENS', 'WC', 'LIFT', 'SEMIN', 'LABO', 'BIBL', 'SEK', 'FEST', 'DEKAN', 'HILF', 'FEUER',
                        'SAMMEL']

    space_map = [{'name':"stieg", "code":79}, {'name':"WC", "code":91}, {'name':"BÜRO", "code":63},
                 {'name':"gang", "code":44},{'name':"aula", "code":4},{'name':"LIFT", "code":33},
                 {'name':"AUFZU", "code":33},{'name':"WC HER", "code":104},{'name':"WC DAM", "code":105},
                 {'name':"SEKR", "code":103}]

    for space in space_map:
        like_name = space['name'].upper()
        s = f"""UPDATE django.buildings_buildingfloorspace set space_type_id = {space['code']} 
                WHERE upper(room_description) like '%{like_name}%' """

        print(s)

        cur.execute(s)
        conn.commit()

    # s = """
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%STIEG%';
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%MENS%'; --mensa
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%WC%';
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%LIFT%';
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%SEMIN%'; --seminarraum
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%LABO%'; --labor
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%BIBL%'; --biblio
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%SEK%'; --sektretariat
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%FEST%';--festsaal
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%DEKAN%'; --dekan
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%HILF%'; --erste hilfe
    # select distinct (room_description) from campuses.indrz_spaces_eg where upper(room_description) like '%FEUER%';
    # select distinct (room_description) from campuses.indrz_spaces_01 where upper(room_description) like '%SAMMEL%';"""



def find_name(floor_num):
    floor_name = ""

    for floor in unique_floor_map:
        if floor['number'] == floor_num:
            floor_name = floor['name']
            break

    if floor_name != "":
        return floor_name
    else:
        return None


def update_floor_name():
    sel = """SELECT floor_num from django.buildings_buildingfloorspace;"""
    cur.execute(sel)

    # rows = cur.fetchall()
    # for row in rows:
    #     floor_num = row[0]
    #     floor_name = find_name(floor_num)

    for floor_num in unique_floor_map:
        floor_name = find_name(floor_num['number'])
        s = f"""UPDATE django.buildings_buildingfloorspace set floor_name = '{floor_name}' where floor_num = {floor_num['number']};"""
        cur.execute(s)
        conn.commit()

    for floor_num in unique_floor_map:
        floor_name = find_name(floor_num['number'])
        s = f"""UPDATE django.poi_manager_poi set floor_name = '{floor_name}' where floor_num = {floor_num['number']};"""
        cur.execute(s)
        conn.commit()


def create_poi_building_letters():
    for floor_name in unique_floor_names:
        floor_float = get_floor_float(floor_name)

        sql = f"""INSERT INTO django.poi_manager_poi (name, floor_num, description, enabled, geom, poi_tags,
name_en, name_de, floor_id, category_id, floor_name, campus_id)
            SELECT name, {floor_float}, description, enabled, geom, poi_tags,
name_en, name_de, floor_id, category_id, '{floor_name}', campus_id  
            FROM django.poi_manager_poi 
            WHERE category_id = 81
            AND floor_name = 'EG' ;"""

        print(sql)

        cur.execute(sql)
        res = conn.commit()


if __name__ == '__main__':
    # create_poi_wings()
    create_poi_building_letters()
    # update_space_type_id()
    # create_poi()

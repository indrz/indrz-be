import psycopg2
from utils import con_string, get_floor_float, unique_floor_names, con_dj_string

conn = psycopg2.connect(con_dj_string)
cur = conn.cursor()




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


if __name__ == '__main__':
    update_space_type_id()
    # create_poi()

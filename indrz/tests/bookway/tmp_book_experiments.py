#
# from django.conf import settings
# settings.configure(settings)
import collections
import json
import re

import psycopg2
from geojson import Feature

db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_passwd = os.getenv('db_passwd')
db_database = os.getenv('db_name')
db_port = os.getenv('db_port')


aau_client_secret=  os.getenv('aau_client_secret')
aau_client_id = os.getenv('aau_client_id')


# from django.conf import settings
#
# settings.configure()

# from settings.secret_settings import db_host, db_user, db_name, db_pwd
# connection = psycopg2.connect(host=db_host, user=db_user, port="5432",
#                               password=db_pwd, database=db_name)



connection = psycopg2.connect(host=db_host, user=db_user, port="5432",
                              password=db_passwd, database=db_name)


# class TestBookSearch(TestCase):
#
#
#     def test_search_for_shelf(self):
#
#         shelf = v.search_for_shelf('HA1/13-6.0.220.11')
#
#         assert shelf

def create_geojson(data, key_value):
    d = collections.OrderedDict()
    d["shelf-id"] = data[0]
    d["m-from"] = data[1]
    d["m-to"] = data[2]
    d['shelf-side'] = data[5]
    d["location"] = (d["m-to"] + d["m-from"]) / 2

    d['offset_value'] = 1

    if d['shelf-side'] == 'R':
        d['offset_value'] = -1

    sql_shelf_geom = """
        SELECT  
            ST_ASGeojson(ST_LineInterpolatepoint(ST_OffsetCurve((ST_Dump(bs.geom)).geom, {offset_value}), 
            {location}/(select max(measure_to) - min(measure_from) as l from bookway.shelfdata WHERE 
                          external_id = '{shelf-id}' limit 1))) as geom,
            bf.floor_num as floor_num, 
            {location}/(select max(measure_to) - min(measure_from) as l from bookway.shelfdata WHERE 
                          external_id = '{shelf-id}' limit 1) as ratio_pos
        FROM
            django.library_bookshelf AS bs
        JOIN django.buildings_buildingfloor AS bf ON (bf.id = bs.fk_building_floor_id)
        WHERE external_id = '{shelf-id}' and measure_from <= {location} and measure_to >= {location}
        """.format(**d)

    # ST_Translate(geometry    g1, float    deltax, float    deltay, float    deltaz)

    cursor = connection.cursor()

    cursor.execute(sql_shelf_geom)

    shelf_res_geo = cursor.fetchone()

    if shelf_res_geo:

        d['floor_num'] = shelf_res_geo[1]
        d['measure'] = shelf_res_geo[2]
        d['key'] = key_value

        n_feature = Feature(geometry=json.loads(shelf_res_geo[0]), properties=d)

        return n_feature
    else:
        return None


def _convert(val):
    try:
        float(val)
        return val
    except ValueError:
        return '"%s"' % val


def search_for_shelf(key_value):
    ky_array = re.split("[^\d\w]+", key_value)

    where_clause = "{%s}" % ",".join(_convert(i) for i in ky_array)

    sql_base = """
        SELECT
          sd.external_id, -- 0
          sd.measure_from, -- 1
          sd.measure_to, -- 2
          bookway.commonness('{0}', sys_von_array) + bookway.commonness('{0}', sys_bis_array) AS commonness, -- 3
          sd.stockwerk, -- 4,
          sd.seite -- 5
        FROM
          bookway.shelfdata AS sd

        WHERE
          '{0}' BETWEEN bookway.equalize_arrays('{0}', sys_von_array, '0') AND bookway.equalize_arrays('{0}', sys_bis_array, 'Z')
          OR bookway.commonness('{0}', sys_von_array) + bookway.commonness('{0}', sys_bis_array) > 0
        ORDER BY
          commonness DESC
        LIMIT 1
    """.format(where_clause)

    cursor = connection.cursor()

    cursor.execute(sql_base)

    shelf_res = cursor.fetchone()

    if shelf_res:
        n_feature = create_geojson(shelf_res, key_value)
        # return n_feature
        if n_feature:
            return n_feature
        else:
            return False
    else:

        # single_items = ['ZLS', 'ZMS', 'ZMU', 'PLM', '2.1']
        #
        # if len(ky_array) <= 2:
        #     if ky_array == "ZLS"

        return False


def test_shelf_search():
    cur = connection.cursor()

    sql = """SELECT DISTINCT systemid FROM bookway.all_sys_data ORDER BY systemid ASC"""

    cur.execute(sql)
    test_data = cur.fetchall()

    no_res = []

    starters = ['HA1', 'ZLS', 'ZMU', 'HSS']

    with open('no-matches-search-shelf.txt', 'w+') as f:

        for key in test_data:

            ky_array = re.split("[^\d\w]+", key[0])
            res = search_for_shelf(key[0])

            if res:
                pass
            else:
                r = key[0].split
                if ky_array[0] in starters:
                    pass
                else:
                    mystring = key[0] + '\n'
                    f.write(str(mystring))


# test_shelf_search()

def create_book_route():

    with open('no-matches.txt', 'r') as test_data:

        with open('no-route-created.txt', 'w+') as f:

            for key in test_data.readlines():
                print(key)

                ky_array = re.split("[^\d\w]+", key[0])
                res = search_for_shelf(key[0])

                print(res)

                if res:
                    pass
                else:
                    mystring = key + '\n'
                    f.write(str(mystring))

create_book_route()
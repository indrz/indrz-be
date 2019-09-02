#!/usr/bin/env python

import psycopg2
import json
import requests
# import urllib2
import json
import os
# from subprocess import call
# import geowebcache_seed
import hashlib
import datetime
import logging

# logging.basicConfig(filename='/opt/update_rooms/roomlog.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.basicConfig(filename='roomlog.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Database Connection Info
#db_host = "137.208.3.187"
db_host = "gis-neu.wu.ac.at"
db_user = "indrz-wu"
#db_user = "postgres"
#db_passwd = "12345"
db_passwd = "QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU"
db_database = "indrz-wu"
#db_port = "5433"
db_port = "5432"

space_type_ids = ("space_type_id", "room_code", "long_name", "room_description", )

create_room_anno_view = """SELECT d.room_code, w.bs_roomnr, w.fancyname_de, w.category_de, d.geom from django.buildings_buildingfloorspace as d, wudata.raumlist_buchungsys as w
WHERE d.room_external_id = w.pk_big;"""

sql_remove_dub_values_roomcode = """UPDATE
                    wudata.raumlist_buchungsys
                    set
                    roomname_de = ''
                    WHERE
                    roomcode = roomname_de;"""

sql_create_view = """SELECT
                        d.id,
                        w.category_de as short_name,
                        w.roomname_de as long_name,
                        w.roomcode as room_code,
                        d.space_type_id,
                        d.geom
                        FROM
                        django.buildings_buildingfloorspace as d, wudata.raumlist_buchungsys as w
                        WHERE
                        d.room_external_id = w.pk_big
                        AND
                        d.floor_num = 4;"""

sql_test_sel = """SELECT
                    roomcode, roomname_de
                    from wudata.raumlist_buchungsys

                    WHERE
                    roomcode = roomname_de;"""

sql_update = """UPDATE
                    wudata.raumlist_buchungsys
                    set
                    roomname_de = ''
                    WHERE
                    roomcode = roomname_de;"""


def bach_get_all_bookable_rooms():
    """

    :return: all rooms available in bach for booking as json in set Result
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus'

    data = {
        'id': '0815',
        'method': 'get_campus2013',
        'params': (),
    }
    #data = simplejson.dumps(data)
    data = json.dumps(data)     # this will encode the data into json format
    headers = {
        'Content-Type': 'application/json-rpc',
    }

    # req = urllib2.Request(url, data, headers)
    rq = requests.post(url, data=data, headers=headers)
    # print(rq.status_code)
    # print(rq.json())
    # resp = urllib2.urlopen(req)
    # data = resp.read().encode('utf-8')
    print(rq.text)
    decoded_json = json.loads(rq.text)   # this will load json data into a python object

    if 'result' in decoded_json:
        return decoded_json['result']
    else:
        return None

# json_data_current= "/opt/update_rooms/all_rooms_current.json"
# json_data_update = "/opt/update_rooms/all_rooms_update.json"

json_data_current= "all_rooms_current.json"
json_data_update = "all_rooms_update.json"

def check_json_for_update():
    data_all_bookable_rooms = bach_get_all_bookable_rooms()
    fo = open(json_data_update, "w")
    fo.write(str(data_all_bookable_rooms))
    fo.close()
# run the download and create new file to test, download the json file and compare to current json
check_json_for_update()  

# check if files have changed

#source http://www.pythoncentral.io/finding-duplicate-files-with-python/
def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def compare_two_files():
    file_1 = hashfile(json_data_current)

    file_2 = hashfile(json_data_update)
    
    if file_1 == file_2:
        print("no changes file all_rooms_current.json equals all_rooms_update.json")
        return True
    else:
        print("yes changes found files not equal")
        return False

#if os.path.getsize(json_data_current) == os.path.getsize(json_data_update):
#    os.remove(json_data_update) # no change so delete the downloaded json file
if compare_two_files() is True:
    os.remove(json_data_update) # no change so delete the downloaded json file
    logging.info('nothing changed today')
    #print('nothing changed')
else:
    print("yes changes")
    logging.info('yes we have changes')
    os.remove(json_data_current)  # new data so remove the current json file
    os.rename(json_data_update, json_data_current)  # rename new downloaded json to be the new current json
    ## NOW update the tables and data with new data
    # get a connection handle to Postgresql queries
    conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)

    # get the cursor
    cur = conn.cursor()

    floor_list = ('ug01_rooms', 'eg00_rooms', 'og01_rooms', 'og02_rooms', 'og03_rooms', 'og04_rooms', 'og05_rooms', 'og06_rooms' )
    #list_room_cols = ('bs_orientierung', 'bs_building', 'bs_floor', 'bs_roomnr', 'bs_fancy_name_de', 'bs_aks_nummer')
    new_room_cols = ('bs_building', 'bs_floor', 'bs_roomnr','buildingolor','capacity','roomname_en','fancyname_de',\
                     'roomname_de','pk_big','category_en','roomcode','tid','fancyname_en','category_de','floorname','buildingname')

    # remove all data in geodata.raum_buchsys
    cur.execute("DELETE FROM wudata.raumlist_buchungsys;")

    # empty all data in bs_.. columns set values to NULL
    # GIS OLD
    # for floor in floor_list:
    #     for bs_columns in new_room_cols:
    #         cur.execute ("UPDATE geodata." + floor + " SET " + bs_columns + " = NULL;")

    # insert new data into columns

    # since we are using placeholders, we really only need to assign the query string sans values once, outside the loop
    query = """INSERT INTO wudata.raumlist_buchungsys (buildingolor,capacity,roomname_en,fancyname_de, \
        roomname_de,pk_big,category_en,roomcode,tid,fancyname_en,category_de,floorname,buildingname) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    all_rooms_json = bach_get_all_bookable_rooms()
    for data in all_rooms_json:
            buildingolor = data['buildingcolor']
            buildingname = data['buildingname']
            capacity = data['capacity']
            category_de = data['category_de']
            category_en = data['category_en']
            fancyname_de = data['fancyname_de']
            fancyname_en = data['fancyname_en']
            floorname = data['floorname']
            pk_big = data['pk_big']
            roomcode = data['roomcode']
            roomname_de = data['roomname_de']
            roomname_en = data['roomname_en']
            tid = data['tid']

            # the row contents
            values = (buildingolor,capacity,roomname_en,fancyname_de,roomname_de,pk_big,category_en,\
                      roomcode,tid,fancyname_en,category_de,floorname,buildingname)
            res = cur.execute(query, values)
            #print str(values)

    # example rn_orientierung -  TC.1.245
    cur.execute("update wudata.raumlist_buchungsys set bs_building = split_part(roomcode, '.', 1);") # is the TC
    cur.execute("update wudata.raumlist_buchungsys set bs_floor = split_part(roomcode, '.', 2);")# is the 1
    cur.execute("update wudata.raumlist_buchungsys set bs_roomnr = split_part(roomcode, '.', 3);") # is the 245 from example

    # update columns with new data
    # for floor in floor_list:
    #     cur.execute ("""UPDATE geodata.""" + floor + """ as b
    #                     SET
    #                       roomcode = a.roomcode,
    #                       bs_building = a.bs_building,
    #                       bs_floor = a.bs_floor,
    #                       bs_roomnr = a.bs_roomnr,
    #                       fancyname_de = a.fancyname_de,
    #                       buildingolor = a.buildingolor,
    #                       capacity = a.capacity,
    #                       category_de = a.category_de,
    #                       roomname_en = a.roomname_en,
    #                       roomname_de = a.roomname_de,
    #                       tid = a.tid,
    #                       category_en = a.category_en,
    #                       fancyname_en = a.fancyname_en,
    #                       floorname = a.floorname,
    #                       buildingname = a.buildingname,
    #                       pk_big = a.pk_big
    #                     FROM geodata.raumlist_buchungsys as a
    #                     WHERE a.pk_big = b.aks_nummer;""")
    #     cur.execute ("UPDATE geodata." + floor + " set bs_roomnr = lpad(bs_roomnr, 3, '0') where length(bs_roomnr) < 3;")

    #call('geowebcache_seed.py')  # this is NOT Pythonic but a way to call another python script from within a python script
    #print('calling geowebcache_seed')
    # geowebcache_seed.reload_geoserver()
    # geowebcache_seed.seed_geowebcache()  # call the geowebcache seed to re-seed all tiles since we have new labels
    # close cursor
    print("DONE")
    cur.close()

    # We are using an InnoDB tables so we need to commit the transaction
    conn.commit()

    #close connection
    conn.close()

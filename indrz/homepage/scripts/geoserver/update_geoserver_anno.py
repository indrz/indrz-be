#!/usr/bin/env python
import hashlib

import os
import psycopg2
import requests
import json
import filecmp

# import geowebcache_seed
import datetime
import logging

try:
    from settings.secret_settings import db_host, db_name, db_port, db_pwd, db_user
except ImportError:
    try:
        from secret_settings import geoserver_pwd, geoserver_user
    except ImportError:
        pass
else:
    pass

from geowebcache_seed import seed_geowebcache

# logging.basicConfig(filename='/opt/update_rooms/roomlog.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.basicConfig(filename='/srv/indrz_logs/roomlog.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Database Connection Info

db_port = "5432"


def bach_get_all_bookable_rooms():
    """

    :return: all rooms available in bach for booking as json in set Result
    """
    url = 'https://campus.aau.at/rooms' # note urls in unknown 

    data = {
        'id': '0815',
        'method': 'get_rooms',
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
    decoded_json = json.loads(rq.text)   # this will load json data into a python object

    if 'result' in decoded_json:
        return rq.text
        # return decoded_json['result']
    else:
        return None


json_data_current= "all_rooms_current.json"
json_data_update = "all_rooms_update.json"



def get_current_set_of_all_rooms():
    data_all_bookable_rooms = bach_get_all_bookable_rooms()
    fo = open(json_data_update, "w")
    fo.write(str(data_all_bookable_rooms))
    fo.close()
# run the download and create new file to test, download the json file and compare to current json
get_current_set_of_all_rooms()


# source http://www.pythoncentral.io/finding-duplicate-files-with-python/
def hashfile(path, blocksize=65536):
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
        logging.info("NO changes")
        return False
    else:
        print("yes changes found files not equal")
        logging.info("YES new changes")
        return True


def update_wu_anno_table():

    ## NOW update the tables and data with new data
    # get a connection handle to Postgresql queries
    conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_pwd, database=db_name)
    cur = conn.cursor()
    cur.execute("DELETE FROM wudata.raumlist_buchungsys;")


    # since we are using placeholders, we really only need to assign the query string sans values once, outside the loop
    query = """INSERT INTO wudata.raumlist_buchungsys (buildingolor,capacity,roomname_en,fancyname_de, \
        roomname_de,pk_big,category_en,roomcode,tid,fancyname_en,category_de,floorname,buildingname) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    text_response = bach_get_all_bookable_rooms()
    all_rooms_json = json.loads(text_response)


    for data in all_rooms_json['result']:
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
        values = (buildingolor, capacity, roomname_en, fancyname_de, roomname_de, pk_big, category_en, \
                  roomcode, tid, fancyname_en, category_de, floorname, buildingname)
        res = cur.execute(query, values)
        # print str(values)

    # example rn_orientierung -  TC.1.245
    cur.execute("update wudata.raumlist_buchungsys set bs_building = split_part(roomcode, '.', 1);")  # is the TC
    cur.execute("update wudata.raumlist_buchungsys set bs_floor = split_part(roomcode, '.', 2);")  # is the 1
    cur.execute(
        "update wudata.raumlist_buchungsys set bs_roomnr = split_part(roomcode, '.', 3);")  # is the 245 from example

    sql_remove_dub_values_roomcode = """UPDATE wudata.raumlist_buchungsys
                                        SET roomname_de = '',
                                            roomname_en = ''
                                        WHERE
                                        roomcode = roomname_de;"""

    cur.execute(sql_remove_dub_values_roomcode)

    cur.close()
    # We are using an InnoDB tables so we need to commit the transaction
    conn.commit()

    #close connection
    conn.close()


if not filecmp.cmp(json_data_current, json_data_update):
    # Compare the files named f1 and f2, returning True if they seem equal, False otherwise.
    logging.info("yes changes found")

    update_wu_anno_table()

    os.remove(json_data_current)  # new data so remove the current json file
    os.rename(json_data_update, json_data_current)  #

    seed_geowebcache()
else:
    os.remove(json_data_update)
    logging.info('no changes found')

# update_wu_anno_table()
# if compare_two_files():
#     update_wu_anno_table()
    # seed_geowebcache()

#!/bin/python
# coding: utf-8
import psycopg2
import time


conn_indrzAau = psycopg2.connect(host='localhost', user='indrz-aau', port='5432', password='oaAcKEGzohkqR2Mj',
                                 database='indrzAau')
cur_indrzAau = conn_indrzAau.cursor()

conn_dev_aau = psycopg2.connect(host='localhost', user='postgres', port='5432', password='air',
                                database='indrzAauLiveOld')
cur_dev_aau = conn_dev_aau.cursor()


table_abrev = ('e00_', 'e01_', 'e02_', 'e03_')
floor_nums = ("0", "1", "2", "3")

INDOORWAY = 0
STAIRWAY = 1
ELEVATOR = 2
ESCALATOR = 3
OUTDOORWAY = 4
RAMP = 5
ZEBRA = 6
STAIRWAY_NO_CHANGE = 101
RAMP_NO_CHANGE = 102
ELEVATOR_NO_CHANGE = 103
ESCALATOR_NO_CHANGE = 104


def get_network_type(old_type):
    old_net_types = [
        {
            "typeid": 0,
            "newid": 0,
            "text": "Wege (Innen)",
            "cost": 1.0
        },
        {
            "typeid": 2,
            "newid": 6,
            "text": "Zebrastreifen",
            "cost": 1.0
        },
        {
            "typeid": 4,
            "newid": 900,
            "text": "Privat",
            "cost": 1.0
        },
        {
            "typeid": 5,
            "newid": 5,
            "text": "Rampe",
            "cost": 1.8
        },
        {
            "typeid": 7,
            "newid": 5,
            "text": "Rampe mit Stockwerkwechsel",
            "cost": 1.9
        },
        {
            "typeid": 1,
            "newid": 1,
            "text": "Stiegen mit Stockwerkwechsel",
            "cost": 4.0
        },
        {
            "typeid": 3,
            "newid": 101,
            "text": "Stiegen ohne Stockwerkwechsel",
            "cost": 4.0
        },
        {
            "typeid": 6,
            "newid": 2,
            "text": "Lift",
            "cost": 10.0
        },
        {
            "typeid": 9,
            "newid": 103,
            "text": "Lift ohne Stockwerkwechsel",
            "cost": 10.0
        },
        {
            "typeid": 8,
            "newid": 4,
            "text": "Wege (im Freien)",
            "cost": 1.3
        }
    ]

    type_id = 0

    for type in old_net_types:

        if old_type is None:
            type_id = 0
            # print(old_type)

            break

        if old_type == 99:
            type_id = 900
            # print(old_type)
            break

        if old_type == type['typeid']:
            type_id = type['newid']
            # print(type_id)


            break

    return type_id


def import_networklines(floor):



    sel_networklines = """
         SELECT cost, type, text, st_multi(st_transform(geom3d, 3857))
       FROM geodata.{0}network_lines""".format(floor)
    # print(sel_networklines)

    cur_dev_aau.execute(sel_networklines)
    # print(sel_networklines)

    res = None
    res = cur_dev_aau.fetchall()
    #print(res)
    floor_num = floor[2:3]
    floor_abr = floor[0:3]


    #
    # print(floor_num)
    # print(floor_abr)

    # q_delete = """DELETE FROM django.routing_networklines{0}""".format(floor_level_txt)
    # cur_dev_aau.execute(q_delete)
    #cur_dev_aau.commit()

    if len(res) > 0:
        for r in res:

            speed = r[0]  # old cost
            old_type = r[1]
            old_name = r[2]
            old_geom = r[3]

            new_net_type = get_network_type(old_type)
            # print(new_net_type)

            acc_type = 'PUBLIC'
            # print(r[0])



            if old_type == 4:
                acc_type = 'PRIVATE'


            insert_state = """INSERT INTO django.routing_networklinese0{0} (speed, network_type, geom, name, floor_num, access_type)
                        VALUES ({1}, {2}, \'{3}\', '{4}', {5}, '{6}')""".format(floor_num, speed, new_net_type, r[3], r[2], floor_num, acc_type)
            # print(insert_state)
            cur_indrzAau.execute(insert_state)
            conn_indrzAau.commit()
            print(insert_state)


def update_network_types(floor):
    floor_level_txt = floor[3:4]
    if floor == "ug01_":
        floor_level_txt = 'ug01'

    print(floor_level_txt)
    if not floor_level_txt == 'ug01':
        floor_level_txt = "e0" + str(floor_level_txt)

    network_types = {'indoor': 0, 'stairway': 1, 'elevator': 2, 'escalator': 3, 'outdoorway': 4,
                     'ramp': 5, 'zebra': 8, 'private': 9, 'stairway_no_change': 101, 'ramp_no_change': 102,
                     'elevator_no_change': 103, 'escalator_no_change': 104}

    # q_sel = """select network_type from django.routing_networklines{0}
    #       where network_type = {1}""".format(floor_level_txt, 1 )
    #
    # print(q_sel)

    q_update = """update django.routing_networklines{0}
        set network_type = {1}
        where network_type = {2}""".format(floor_level_txt, network_types['stairway'], 3)

    print(q_update)
    cur_dev_aau.execute(q_update)
    conn_dev_aau.commit()



for floor in table_abrev:
    import_networklines(floor)


import csv
import os
import json
from django.contrib.gis.gdal import DataSource, SpatialReference
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon

import pandas as pd
import psycopg2
from pathlib import Path

from utils import con_string, con_dj_string, unique_floor_names


conn = psycopg2.connect(con_string)
cur = conn.cursor()


conn_dj = psycopg2.connect(con_dj_string)
cur_dj = conn_dj.cursor()

campus_name_map = \
campuses = ['Karlsplatz', 'Getreidemarkt', 'Gusshaus', 'Freihaus', 'Arsenal', 'Ausweichquartier']
csv_campuses = ['A_KARLSPLATZ', 'B_GETREIDEMARKT', 'C_GUSSHAUS', 'D_FREIHAUS', 'O_ARSENAL', 'W_AUSWEICHQUARTIER']

campuses_dict = dict(zip(campuses, csv_campuses))

# def drop_all_dj_tables():
#
#     table_names = ['buildings_buildingfloorspace', 'building_buildingfloorplanline', 'building_buildingfloor',
#                    'building_building', 'building_campus', 'building_organization']
#
#     for table_name in table_names:
#         s = f"""DROP TABLE django.{table_name};"""
#         cur_dj.execute(s)
#         conn_dj.commit()


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


# read_all_spaces_csv()

def read_campus_floors(campus_name):

    campus_data = {}
    df = pd.read_csv('gebauede-tu-juli-2019.csv',header=None, names=["CAMPUS","TRAKT","TRAKTBEZEICHNUNG","ADRESSE","PLZ","ORT","GESCHOSS"], delimiter=";")
    # print(df.groupby('TRAKT').groups)

    grouped_campus = df.groupby('CAMPUS')
    campuses = [name for name, group in grouped_campus]

    for campus in campuses:
        if campus == campus_name:
            c = df[df['CAMPUS'].str.contains(campus)]
            # print(campus, len(c))

            trak = c.groupby('TRAKT')
            trakts = [name for name, group in trak]
            # print("TRACKTS ", trakts, " count: ", len(trakts))
            campus_data['traks'] =  {'all': trakts}
            campus_data['traks']['count'] = len(trakts)

            gp_floors = c.groupby('GESCHOSS')
            floors = [name for name, group in gp_floors]
            # print(f"FLOORS on {campus} campus ", floors, " count: ", len(floors))
            campus_data['num_floors'] = len(floors)

            address = c.groupby('ADRESSE')
            adresses = [name for name, group in address]

            # print("adresses ", " count : ", len(adresses), " adresses ", adresses)
            campus_data['adresses'] = {'all':adresses}
            campus_data['adresses']['count'] = len(adresses)

            campus_data['buildings'] = []
            for a in adresses:
                print(a)
                campus_data['a'] = {}
                campus_data['a']['adress'] = a
                campus_data['a']['campus'] = campus

                t = df[df['ADRESSE'].str.contains(a)]

                gp2_floors = t.groupby('GESCHOSS')
                floors2 = [name for name, group in gp2_floors]



                t_data = []
                # for key, group_df in t.groupby('TRAKT'):
                    # print("the group for product '{}' has {} rows".format(key, len(group_df)))
                    # print("values each trakt is : ", group_df.values)

                x = t.groupby('TRAKT')
                tt = [name for name, group in x]
                print("address ", a, " tracks at this address ", tt, " floors ", floors2,)
                campus_data['a']['trakts'] = tt
                campus_data['a']['floors'] = floors2
                campus_data['buildings'].append(campus_data['a'])
                # print(campus_data['a'])

    return campus_data


# print(read_campus_floors('C_GUSSHAUS'))

def read_campus_csv_list():
    df = pd.read_csv('gebauede-tu-juli-2019.csv',header=None, names=["CAMPUS","TRAKT","TRAKTBEZEICHNUNG","ADRESSE","PLZ","ORT","GESCHOSS"], delimiter=";")
    # print(df.groupby('TRAKT').groups)

    grouped_campus = df.groupby('CAMPUS')
    grouped_trakt = df.groupby('TRAKT')
    grouped_adresse = df.groupby('ADRESSE')
    grouped_floors = df.groupby('GESCHOSS')

    campuses = [name for name, group in grouped_campus]
    print(campuses)
    trakts = [name for name, group in grouped_trakt]
    adresse = [name for name, group in grouped_adresse]
    floors = [name for name, group in grouped_floors]

    print("floors", len(floors), floors)
    print("campuses", len(campuses))
    print("trakts", len(trakts))
    print("adresse", len(adresse))

    for campus in campuses:
            if campus != 'CAMPUS':
                    c = df[df['CAMPUS'].str.contains(campus)]
                    print(campus, len(c))

                    trak = c.groupby('TRAKT')
                    trakts = [name for name, group in trak]
                    print("TRACKTS ", trakts, " count: ", len(trakts))


                    gp_floors = c.groupby('GESCHOSS')
                    floors = [name for name, group in gp_floors]
                    print(f"FLOORS on {campus} campus ", floors, " count: ", len(floors))


                    address = c.groupby('ADRESSE')
                    adresses = [name for name, group in address]
                    print("adresses ", " count : ", len(adresses), " adresses ", adresses)


                    for a in adresses:
                        t =df[df['ADRESSE'].str.contains(a)]

                        gp2_floors = t.groupby('GESCHOSS')
                        floors2 = [name for name, group in gp2_floors]

                        x = t.groupby('TRAKT')
                        tt = [name for name, group in x]
                        print("address-new ", a, " tracks at this address ", tt, " floors ", floors2)


# read_campus_csv_list()


def create_org():
    sql_org = f"""INSERT INTO django.buildings_organization (name, street, house_number) VALUES ('Technische Universität Wien', 'Karlsplatz', '13');"""
    cur_dj.execute(sql_org)
    conn_dj.commit()



def create_campus():

    organization_id = 1

    campuses = ['Karlsplatz', 'Getreidemarkt', 'Gusshaus', 'Freihaus', 'Arsenal', 'Ausweichquartier']

    for campus in campuses:
        sql_campus = f"""INSERT INTO django.buildings_campus (campus_name, fk_organization_id) VALUES ('{campus}', {organization_id})"""
        cur_dj.execute(sql_campus)
        conn_dj.commit()


def create_building():

    # for campus in campuses_dict:
    #
    sql_campus = f""" SELECT id, fk_organization_id, campus_name from django.buildings_campus;"""
    cur_dj.execute(sql_campus)
    campuses = cur_dj.fetchall()

    for campus in campuses:
        print(campus)
        org_id = campus[1]
        campus_id = campus[0]
        campus_name = campus[2]

        print(campus_name)

        c = campuses_dict[campus_name]

        x = read_campus_floors(c)

        # print("yo x ", x['buildings'])

        for building in x['buildings']:
            adress = building['adress']
            traks = building['trakts']
            floors = building['floors']
            b_num_floors = len(building['floors'])
            name = traks[0][0].upper()

            # print(adress, traks, floors, b_num_floors)

            sql_building = f"""INSERT INTO django.buildings_building (name, street, num_floors, description, fk_organization_id, fk_campus_id, wings)
                        VALUES ('{name}', '{adress}', {b_num_floors}, '{json.dumps(floors)}', {org_id}, {campus_id}, '{json.dumps(traks)}');"""

            print(sql_building)
            cur_dj.execute(sql_building)
            conn_dj.commit()


def create_floor():

    for floor in unique_floor_names:
        floor_float = get_floor_float(floor)
        building_id = 1
        floor_name = floor

        sql_insert = f"""INSERT INTO django.buildings_buildingfloor (short_name, long_name, floor_num, geom, fk_building_id) 
                                    SELECT '{floor}', short_name,{floor_float}, st_setsrid(st_transform(geom,3857), 3857),
                                     {building_id} 
                                     FROM campuses.indrz_umriss_eg""";

        cur_dj.execute(sql_insert)
        conn_dj.commit()


def update_values():
    for floor in unique_floor_names:

        fake_tag = "{xx_" + floor +"_xx_xxx, xx_xxx}"
        empty_array = "'{}'"

        sql = f"""update campuses.indrz_spaces_{floor} set tags = '{fake_tag}'  where tags isnull or tags = {empty_array};"""
        cur_dj.execute(sql)
        conn_dj.commit()
        print(sql)


def create_space(floors):

    for floor in floors:
        floor_id = 1
        floor_name = floor

        sql_insert = f"""INSERT INTO django.buildings_buildingfloorspace (room_external_id, room_description, floor_num,
                                    long_name, short_name, tag, geom, fk_building_floor_id, space_type_id)
                                    SELECT room_external_id, room_description, floor_num, long_name, short_name,
                                     tags, st_setsrid(st_transform(geom,3857), 3857), {floor_id}, space_type_id 
                                     FROM campuses.indrz_spaces_{floor_name}
                     """
        print(f"now on floor {floor}")
        cur_dj.execute(sql_insert)
        conn_dj.commit()


def populate_space_attributes():


    s = f"""update django.buildings_buildingfloorspace set short_name = substring(room_external_id,4,2) where floor_num ISNULL;"""
    cur_dj.execute(s)
    conn_dj.commit()

    sel = """SELECT short_name, tag, id, room_external_id from django.buildings_buildingfloorspace """
    cur_dj.execute(sel)
    spaces = cur_dj.fetchall()

    print("the space is ", spaces)
    for space in spaces:
        id = space[2]
        if space[1] and space[1] != '{}':
            floor_name = space[1].split('_')[-4]
            floor_float = get_floor_float(floor_name)

            print(floor_name, floor_float)
            sql_update = f"""update django.buildings_buildingfloorspace set floor_num = {floor_float}, long_name = '{floor_name}'
            WHERE floor_num ISNULL AND id = {id};"""
            cur_dj.execute(sql_update)
            conn_dj.commit()

        elif space[3] and space[3] != '':
            floor_name = space[3].split(' ')[1]
            floor_float = get_floor_float(floor_name)

            sql_update = f"""update django.buildings_buildingfloorspace set floor_num = {floor_float}, long_name = '{floor_name}'
            WHERE floor_num ISNULL AND id = {id};"""
            cur_dj.execute(sql_update)
            conn_dj.commit()

            print("done space ", space)

    sql_update_roomcode = f"""
         update django.buildings_buildingfloorspace set room_code = replace(room_external_id, ' ', '') WHERE 1=1;
         update django.buildings_buildingfloorspace set short_name = room_external_id WHERE 1=1;
         delete from django.buildings_buildingfloorspace where geom ISNULL;
     """
    cur_dj.execute(sql_update_roomcode)
    conn_dj.commit()


def load_cartolines():
    for floor in unique_floor_names:
        floor_id = 1
        floor_name = floor
        floor_float = get_floor_float(floor_name)

        sql_insert = f"""INSERT INTO django.buildings_buildingfloorplanline (floor_name, short_name, long_name, floor_num,
                                     geom, fk_building_floor_id)
                                    SELECT '{floor}', tags, long_name, {floor_float}, st_setsrid(st_transform(geom,3857), 3857), {floor_id} 
                                     FROM campuses.indrz_lines_{floor_name}

                     """
        print(f"now on floor {floor}")
        cur_dj.execute(sql_insert)
        conn_dj.commit()

        sql_remove_empty = f"""
             delete from django.buildings_buildingfloorplanline where geom ISNULL;
         """
        cur_dj.execute(sql_remove_empty)
        conn_dj.commit()



if __name__ == "__main__":
    # NOTE TO SELF
    # NONE of these command delete data only insert
    # execute only if run as a script
    # create_org()
    # create_campus()
    # create_building()
    # create_floor()
    update_values()
    create_space(unique_floor_names)
    populate_space_attributes()
    # load_cartolines()
    print("done")




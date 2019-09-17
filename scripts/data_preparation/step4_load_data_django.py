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

print(con_string)
conn = psycopg2.connect(con_string)
cur = conn.cursor()


print(con_dj_string)
conn_dj = psycopg2.connect(con_dj_string)
cur_dj = conn_dj.cursor()

campus_name_map = \
campuses = ['Karlsplatz', 'Getreidemarkt', 'Gusshaus', 'Freihaus', 'Arsenal', 'Ausweichquartier']
csv_campuses = ['A_KARLSPLATZ', 'B_GETREIDEMARKT', 'C_GUSSHAUS', 'D_FREIHAUS', 'O_ARSENAL', 'W_AUSWEICHQUARTIER']

campuses_dict = dict(zip(campuses, csv_campuses))

print("WHHHAAAT ", campuses_dict['Karlsplatz'])



print(campuses_dict)


def read_all_spaces_csv():
    campus_data = {}

    df = pd.read_csv('AlleRNrnBez12092019.csv', delimiter=";")

    f = df.to_dict()

    for x in f:
        print(x)
        break

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

# create_org()

def create_campus():

    organization_id = 1

    campuses = ['Karlsplatz', 'Getreidemarkt', 'Gusshaus', 'Freihaus', 'Arsenal', 'Ausweichquartier']

    for campus in campuses:
        sql_campus = f"""INSERT INTO django.buildings_campus (campus_name, fk_organization_id) VALUES ('{campus}', {organization_id})"""
        cur_dj.execute(sql_campus)
        conn_dj.commit()


# create_campus()

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

            # print(adress, traks, floors, b_num_floors)


            sql_building = f"""INSERT INTO django.buildings_building (street, num_floors, description, fk_organization_id, fk_campus_id)
                        VALUES ('{adress}', {b_num_floors}, '{json.dumps(traks)}', {org_id}, {campus_id});"""

            print(sql_building)
            cur_dj.execute(sql_building)
            conn_dj.commit()



# create_building()

def create_floor():
    sql_foor = f""" SELECT id, fk_campus_id from django.buildings_building;"""
    cur_dj.execute(sql_floor)
    campuses = cur_dj.fetchall()
    pass

def create_space():
    pass

def create_cartolines():
    pass



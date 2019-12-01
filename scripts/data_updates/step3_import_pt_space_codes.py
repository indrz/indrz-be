from scripts.data_updates.step2_upload_dxf_data import get_dxf_fullpath >import pandas as pd
import os
from django.contrib.gis.gdal import DataSource, SpatialReference
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon

import psycopg2
from pathlib import Path

from utils import unique_floor_names, con_string

conn = psycopg2.connect(con_string)
cur = conn.cursor()


# pnt = GEOSGeometry('POINT(5 23)')
# pnt_v2= Point(5,23)
# print(GEOSGeometry('POINT (0 0)', srid=4326))
# geo_pt = Point(row['Position X'], row['Position Y'], srid=31259)





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





def step2_assign_codes_to_spaces(campus, floors):
    """

    :param campus:  name of the campus
    :param floors: list of floor names
    :return: import donet
    """

    # sql_space = f"""SELECT id, geom FROM campuses.indrz_spaces_{floor}; """

    for floor in floors:

        sql_space = f""" SELECT DISTINCT s.id, s.tags, ST_asewkt(s.geom)
                        FROM campuses.indrz_spaces_{floor.lower()} as s
                        JOIN campuses.indrz_imported_roomcodes as p
                        ON ST_Intersects(s.geom, p.geom)
                        WHERE p.floor_name = '{floor}';"""

        sql_pts = f"""SELECT p.id, p.campus, p.floor_name, p.room_external_id, p.room_code, p.room_text, p.geom, p.room_description, p.cad_layer_name
                        FROM campuses.indrz_imported_roomcodes as p
                        JOIN campuses.indrz_spaces_{floor.lower()} as s
                        ON ST_Intersects(s.geom, p.geom)
                        WHERE p.floor_name = '{floor}';"""
                        # AND p.room_external_id != 'nan';"""

        cur.execute(sql_space)
        spaces = cur.fetchall()

        p = cur.execute(sql_pts)
        points = cur.fetchall()

        print("spaces len ", len(spaces))
        print("points len ", len(points))

        # for point in points:
        #     print(point)

        pts_in = []
        pts_with_id = []
        total_spaces_udated = []

        # list of spaces with 1 or more points inside
        for space in spaces:
            space_geom = GEOSGeometry(space[2])
            space_id = space[0]

            done = False

            for point in points:
                pt_geom = GEOSGeometry(point[6])

                if pt_geom.within(space_geom):
                    # print("your are in ", point)

                    ext_id = point[3]
                    room_des = point[7]
                    room_code = point[4]
                    room_text = point[5]
                    cad_layer_name = point[8]

                    # prio 1 if not nan take value and move on
                    if ext_id != 'nan' and is_roomcode(ext_id):

                        pts_with_id.append(point)
                        update_sql = f"""UPDATE campuses.indrz_spaces_{floor.lower()} 
                                        SET room_external_id = '{ext_id}', room_description = '{room_des}' 
                                        WHERE id = {space_id};"""
                        # print(update_sql)

                        cur.execute(update_sql)
                        conn.commit()

                        total_spaces_udated.append(space_id)

                        done = True
                        break
                    elif is_roomcode(room_code) and ext_id == 'nan' and cad_layer_name != 'GUT_RAUMSTEMPEL':
                        update_sql = f"""UPDATE campuses.indrz_spaces_{floor.lower()}
                                         SET room_external_id = '{room_code}', room_description = '{room_des}'
                                         WHERE id = {space_id};"""
                        # print(update_sql)

                        cur.execute(update_sql)
                        conn.commit()
                        done = True

                        total_spaces_udated.append(space_id)
                        break
                    # elif is_roomcode(room_text) and room_text != 'nan' and cad_layer_name != 'GUT_RAUMSTEMPEL':
                    #     update_sql = f"""UPDATE campuses.indrz_spaces_{floor.lower()}
                    #                      SET room_external_id = '{room_text}', room_description = '{room_des}'
                    #                      WHERE id = {space_id};"""
                    #     # print(update_sql)
                    #
                    #     cur.execute(update_sql)
                    #     conn.commit()
                    #     done = True
                    #
                    #     total_spaces_udated.append(space_id)
                    #     break

                    pts_in.append(point)
            if done:
                continue

        print("total updated is ", len(total_spaces_udated))


karlsplatz_floors = ['01', '02', '03', '04', '05', 'DG', 'EG', 'U1', 'U2', 'Z1', 'Z2', 'Z3', 'Z4', 'ZD', 'ZE', 'ZU'] #  count:  16
getreidemarkt_floors = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', 'DG', 'EG', 'U1', 'U2', 'Z4', 'Z5', 'ZE', 'ZU'] #  count:  19
gusshaus_floors = ['01', '02', '03', '04', '05', '06', '07', 'DG', 'EG', 'SO', 'U1', 'U2', 'Z2', 'ZE'] #  count:  14
freihaus_floors = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'U1', 'U2', 'U3', 'U4', 'ZE', 'ZU']#  count:  20
arsenal_floors = ['01', '02', '03', 'EG', 'U1', 'U2', 'ZE']#   count:  7


if __name__ == '__main__':

    # step1_import_csv_roomcodes('Arsenal') # done 11.09.2019
    # step2_assign_codes_to_spaces('Arsenal', arsenal_floors) # done on 11.09.2019

    # step1_import_csv_roomcodes('Gusshaus')# done on 11.09.2019
    # step2_assign_codes_to_spaces('Gusshaus', gusshaus_floors) # done on 11.09.2019

    # step1_import_csv_roomcodes('Freihaus')# done on 11.09.2019
    # step2_assign_codes_to_spaces('Freihaus', freihaus_floors) # done on 11.09.2019

    # step1_import_csv_roomcodes('Getreidemarkt') # done on 12.09.2019
    # step2_assign_codes_to_spaces('Getreidemarkt', getreidemarkt_floors) # done on 12.09.2019

    # step1_import_csv_roomcodes('Karlsplatz')  # done 23.09.2019 08:36 imported
    # step2_assign_codes_to_spaces('Karlsplatz', karlsplatz_floors)  # done 23.09.2019 08:36 imported

    # step1_import_csv_roomcodes('Getreidemarkt')
    # step2_assign_codes_to_spaces('Getreidemarkt', ['02'])  # done 23.09.2019 08:36 imported

    conn.close()

    # priority 1 CASE 1
    # POINT is INSIDE a SPACE Polygon

    # if 1 point in polygon
    # if room_external_id has a value this takes priority  source cad layer GUT_RAUMSTEMPL
    # else check
    # if 1 or more points in  space and both have this filled take first one
    # if 1 or more points in space and only one has filled take it and move on ignore other

    # case 2 Multiple points in one space
    # a room_external_id value is good :)  take it move on

    # case 3 Multiple points in once space
    # room_external_id value empty
    # check room_code if good take it
    # if room_code empty check room_text if good take it

    # else bail no data

    # GUT_RAUMSTEMPLE has no roomcode

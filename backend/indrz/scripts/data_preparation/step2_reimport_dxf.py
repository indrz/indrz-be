import logging
import os
import subprocess
from pathlib import Path

import psycopg2

from aau_all_rooms_api import AauRoomsApi
from cad_layer_constants import cad_spaces_names, cad_layer_names, cad_construction_names, \
    building_code_map, room_types, category_types
from aau_custom_import_rules import special_room_import_rule
from step2_load_dxf import dxf2postgis
from step7_auto_filesync import new_dxf_files
from utils import get_dxf_fullpath, get_dxf_files, get_floor_str
from utils import get_floor_float, con_dj_string

base_log_path = os.getenv('LOGFILE_DIR')
#/usr/src/app/logs/indrz_roomlog.log
logging.basicConfig(filename=f'{base_log_path}/log_reimport_dxf.log', level=logging.INFO, format='%(asctime)s %(message)s')



def clean_geoms():
    logging.info("removing eroneous geometries")

    remove_long_planlines = """delete from django.buildings_buildingfloorplanline where st_length(geom)>1000;"""
    cur.execute(remove_long_planlines)

    remove_short_planlines = """delete from django.buildings_buildingfloorplanline where st_length(geom) < 0.001"""
    cur.execute(remove_short_planlines)

    remove_large_room = """delete from django.buildings_buildingfloorspace where st_area(geom) > 4500"""
    cur.execute(remove_large_room)

    remove_small_rooms = """delete from django.buildings_buildingfloorspace where st_area(geom) < 1"""
    cur.execute(remove_small_rooms)

    # big polygon near z.0.10
    remove_room_1 = """select st_area(geom), id from django.buildings_buildingfloorspace where st_area(geom) = 86.30824653027554 and room_code is null;"""
    cur.execute(remove_room_1)


    # remove sliver like polygons ie walls or polygons then long (carefull could be a long hallway
    # area buffer negative is good

    # https://gis.stackexchange.com/questions/316128/identifying-long-and-narrow-polygons-in-with-postgis
    # This is also called "shape index". The square of the perimeter divided by the area has a minimum
    # value of 4*Pi() (in the case of a disk, which is the most compact 2D geometry), so it can be
    # normalized by 4*Pi() for an easy interpretation (normalized values close to 1 then mean that
    # you have very compact objects and squares have a values of approximately 1.27).
    remove_walls_from_spaces = """
    DELETE FROM django.buildings_buildingfloorspace
        WHERE room_code IS NULL
        AND st_area(geom)/st_perimeter(geom)^2 < 0.01
    """
    cur.execute(remove_walls_from_spaces)
    conn.commit()


def import_capacity():
    sql_set_capacity = """update django.buildings_buildingfloorspace fs set capacity = tc.capacity::integer
                           from geodata.aau_nightly_data tc
                           where tc.roomcode = room_code;
        """

    cur.execute(sql_set_capacity)
    conn.commit()


def insert_spaces(table, dxflayername, campus='dxf_tables'):
    """
    dxflayername is the layer name in autocad
    """

    floor = table.stem.split('_')[-1]
    building_name = table.stem.split('_')[1]
    floor_name = floor.lower()
    floor_num = get_floor_float(floor)
    campus_table = f"{campus.lower()}.{table.stem.lower()}"

    default_floor_id = 92
    # default_building_id = 2

    print(f"inserting pre_django spaces {table.stem}")
    dest_table_name_spaces = f"indrz_spaces_{floor}"

    # sql_spaces = f"""INSERT INTO pre_django.{dest_table_name_spaces}(long_name, tags, geom)
    #                 SELECT layer, ARRAY['{table.stem}', layer],
    #                st_multi(st_buildarea(st_forceclosed(wkb_geometry)))
    #                -- st_multi(st_makepolygon(st_forceclosed(st_linemerge(wkb_geometry))))
    #
    #             FROM {campus_table}
    #             WHERE ST_NPoints(wkb_geometry) >= 4
    #             AND layer in ('{cad_spaces_names}')"""
    #
    # cur.execute(sql_spaces)

    # new as of 13.05.2021
    # creates spaces with holes ie for elevators or other spaces
    # this ensures NO overlapping polygons ie no overlapping spaces
    try:
        if len(dxflayername) == 1:
            dxflayername = f"('{dxflayername[0]}')"

        sql_spaces_new = f"""

            INSERT INTO pre_django.{dest_table_name_spaces}(long_name, tags, geom)
                SELECT '{table.stem.lower()}', 
                ARRAY['{table.stem}'],
                st_multi(st_makevalid((d).geom)) as geom
                FROM (select st_dump(geom) as d
                      FROM (select st_collectionextract(st_polygonize(geom),3) as geom
                        FROM (SELECT ST_union(geom) geom
                              FROM(SELECT st_forceclosed(st_makevalid(wkb_geometry)) as geom
                                    FROM {campus_table} df
                                     WHERE ST_NPoints(wkb_geometry) >= 4
                                      AND layer in {dxflayername}
                                      AND ST_isvalid(st_makevalid(wkb_geometry)) = True
                                       )
                              as f)
                            As a)
                          as x )
                      as g where ST_isvalid(st_makevalid((d).geom)) = True;
                        """
        print("inserting into pre_django ", campus_table)
        cur.execute(sql_spaces_new)
        conn.commit()

        ###  INSERT SPACES #######

        print(f"inserting DJANGO SPACES {table.stem}")
        sql_dj_spaces = f"""INSERT INTO django.buildings_buildingfloorspace(long_name, tags, geom, floor_num,
                                floor_name, fk_building_floor_id, fk_building_id)
                        SELECT tags[2], tags,
                        st_setsrid(st_transform(geom, 3857), 3857),
                        {floor_num}, 
                        '{floor}', 
                        (select id from django.buildings_buildingfloor where floor_num = {floor_num} 
                                and fk_building_id = (select id from django.buildings_building where name = '{building_name}')  ) as fk_building_floor_id,
                        (select id from django.buildings_building where name = '{building_name}') as fk_building_id
                    FROM pre_django.{dest_table_name_spaces}
                    WHERE tags[1] = '{table.stem}'
                    """
        cur.execute(sql_dj_spaces)
        conn.commit()

        cur.execute(f"""Update django.buildings_buildingfloorspace AS s
                SET room_code = pt.room_code, room_description = pt.room_code, room_external_id = pt.room_external_id
                FROM pre_django.indrz_labels_{floor_name.lower()} AS pt
                WHERE st_contains(s.geom, st_transform(pt.geom, 3857))
                AND s.floor_num = {floor_num};""")
        conn.commit()

        # cur.execute(f"""update django.buildings_buildingfloorspace fs set room_code = room_external_id where room_code is not NULL;""")

        cur.execute(f"""update django.buildings_buildingfloorspace fs set room_description = room_external_id
                                       where room_description is NULL or room_description = '0';""")
        conn.commit()

        cur.execute(f"""update django.buildings_buildingfloorspace fs set fk_building_id = floor.fk_building_id
                                           from django.buildings_buildingfloor floor
                                           where st_contains(st_buffer(floor.geom,0.1), fs.geom)
                                            and fs.floor_num = floor.floor_num;""")
        conn.commit()


        # cur.execute(f"""
        #
        #     update django.buildings_buildingfloorspace fs set room_description = tc.fancyname_de, short_name = tc.roomname_de
        #                        from geodata.aau_nightly_data tc
        #                        where tc.roomcode = room_code;
        #
        #     update django.buildings_buildingfloorspace fs set room_description = room_code
        #                                where room_description is null;
        #
        #     update django.buildings_buildingfloorspace fs set long_name = tc.zusatzbezeichnung
        #                                from geodata.allrooms2023 tc
        #                                where tc.raumnr_schild = room_code
        #                                 and tc.zusatzbezeichnung is not null;
        #
        #     update django.buildings_buildingfloorspace fs set fk_building_id = 7
        #        WHERE fs.room_code like 'N.%';
        #     update django.buildings_buildingfloorspace fs set fk_building_id = 6
        #        WHERE fs.room_code like 'V.%';
        #     update django.buildings_buildingfloorspace fs set fk_building_id = 2
        #        WHERE fs.room_code like 'S.%';
        #     update django.buildings_buildingfloorspace fs set fk_building_id = 3
        #        WHERE fs.room_code like 'L.%';
        #     update django.buildings_buildingfloorspace fs set fk_building_id = 8
        #        WHERE fs.room_code like 'Z.%';
        #     update django.buildings_buildingfloorspace fs set fk_building_id = 4
        #         WHERE fs.room_code like 'O.%';
        # """)
        # conn.commit()


    except Exception as err:
        print("Oops! An exception has occured:", err)

    # USE this only if a label exists for each space
    # IF NOT then NO poly is created so not usefull  yet
    # many polys exist but have no roomcode

    # sql_dj_spaces_new = f"""INSERT INTO django.buildings_buildingfloorspace(room_code, room_description,
    #                         long_name, tags, geom, floor_num,
    #                         floor_name, fk_building_floor_id)
    #                 SELECT pt.room_code, pt.long_name, s.tags[2], s.tags,
    #                 st_setsrid(st_transform(s.geom, 3857), 3857),
    #                 {floor_num}, '{floor}', 1
    #             FROM pre_django.indrz_spaces_{floor} as s
    #             JOIN pre_django.indrz_labels_{floor} as pt ON st_contains(s.geom, pt.geom)
    #             WHERE s.tags[1] = '{table.stem}';
    #             """
    #
    # cur.execute(sql_dj_spaces_new)
    # conn.commit()

    # this query does work, generates lots of polys with no roomcode ie walls turn to polys
    # need to remove all polys with NO roomcode
    # sql_space_with_holes = f"""
    # 	select (d).path[1] as id, st_makevalid((d).geom) as geom


# from (select st_dump(geom) as d
# 	  from (select st_collectionextract(st_polygonize(geom),3) as geom
#         FROM (SELECT ST_union(geom) geom
# 			  FROM(SELECT st_forceclosed(wkb_geometry) as geom
#                     FROM karlsplatz.aa_ab_ac_ad_ae_af_ag_ai_eg_ip_112018 df
#                      WHERE ST_NPoints(wkb_geometry) >= 4
#                       AND layer in ({cad_spaces_names})
#                       AND ST_GeometryType(wkb_geometry)='ST_MultiLineString')
# 			  as f)
# 			As a)
# 	      as x)
# 	  as g;
# """

# test code for holes
# sql_spaces_new = f"""
# INSERT INTO pre_django.{dest_table_name_spaces}(geom)
# select st_multi((st_dump(geom)).geom) as geom from
#     (select st_collectionextract(st_polygonize(geom),3) as geom
#         FROM
#         (SELECT ST_union(geom) geom FROM
#            (SELECT wkb_geometry as geom
#                         FROM {campus.lower()}.{table.stem} df
#              WHERE ST_NPoints(wkb_geometry) >= 4
#                 AND layer in ('{cad_spaces_names}')
#                 AND ST_GeometryType(wkb_geometry)='ST_MultiLineString') as f) As a) as x;
#
# """
# cur.execute(sql_spaces_new)
#
# sql_setspace_tags = f"""
#     update pre_django.{dest_table_name_spaces}
#         set tags = ARRAY['{table.stem}', '{cad_spaces_names}'],
#             long_name = '{cad_spaces_names}'
# """
# cur.execute(sql_setspace_tags)
#
# conn.commit()
#

# TODO  test if create donoughts works
# here is test code
# sql_spaces_new_test = f"""
# INSERT INTO pre_django.{dest_table_name_spaces}(geom)
# select st_multi((st_dump(geom)).geom) as geom from
#     (select st_collectionextract(st_polygonize(geom),3) as geom
#         FROM
#         (SELECT ST_union(geom) geom FROM
#            (SELECT wkb_geometry as geom
#                         FROM {campus.lower()}.{table.stem} df
#              WHERE ST_NPoints(wkb_geometry) >= 4
#                 AND layer in ('{cad_spaces_names}')
#                 AND ST_GeometryType(wkb_geometry)='ST_MultiLineString') as f) As a) as x;
#
# """
#
# sql_setspace_tags = f"""
#     update pre_django.{dest_table_name_spaces}
#         set tags = ARRAY['{table.stem}', '{cad_spaces_names}'],
#             long_name = '{cad_spaces_names}'
# """
# cur.execute(sql_setspace_tags)


def insert_campus_lines(table, campus='dxf_tables'):
    floor = table.stem.split('_')[-1]
    floor_name = floor.lower()
    floor_numzz = get_floor_float(floor)
    campus_table = f"{campus.lower()}.{table.stem.lower()}"

    print(f"inserting lines {table.stem}")
    tablename_lines_floor = f"indrz_lines_{floor}"

    sql_lines = f"""INSERT INTO pre_django.{tablename_lines_floor}(floor_num, long_name, tags, geom)
                        SELECT {floor_numzz}, layer, ARRAY['{table.stem}', layer], wkb_geometry
                        FROM {campus_table}
                        WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                        AND layer in {cad_layer_names};"""
    cur.execute(sql_lines)
    conn.commit()


def insert_construction(table, campus='dxf_tables'):
    floor = table.stem.split('_')[-1]
    floor_num = get_floor_float(floor)

    print(f"inserting CONSTRUCTION AREAS {table.stem}")
    sql_dj_construction = f"""INSERT INTO django.buildings_interiorfloorsection(short_name, long_name, tags, geom,
                                floor_num, floor_name, fk_building_floor_id)
                        SELECT 'Construction', layer, ARRAY['{table.stem}', layer], 
                               st_setsrid(st_multi(st_buildarea(st_transform(st_forceclosed(wkb_geometry), 3857))), 3857),
                                --st_multi(st_makepolygon(st_linemerge(st_forceclosed(wkb_geometry)))),
                                     {floor_num}, '{floor}', 92
                        FROM {campus.lower()}.{table.stem} 
                        WHERE ST_NPoints(wkb_geometry) >= 4
                        -- do not import construction polygons that are very small they are acad icons and not areas
                        -- st_area(geom) > 19 will ensure only true construction areas are created
                        AND st_area(st_setsrid(st_multi(st_buildarea(st_transform(st_forceclosed(wkb_geometry), 3857))), 3857)) > 72
                        AND layer in ('{cad_construction_names}')"""
    cur.execute(sql_dj_construction)
    conn.commit()

    # remove holes in construction areas caused by dxf  symbols
    print(f"removing holes in CONSTRUCTION AREAS {table.stem}")
    sql_update_ifs = f"""UPDATE django.buildings_interiorfloorsection t
                                SET geom = a.geom
                                FROM (
                                    SELECT id, ST_Collect(ST_MakePolygon(geom)) AS geom
                                    FROM (
                                        SELECT id, ST_NRings(geom) AS nrings,
                                            ST_ExteriorRing((ST_Dump(geom)).geom) AS geom
                                        FROM django.buildings_interiorfloorsection
                                        WHERE ST_NRings(geom) > 1
                                        ) s
                                    GROUP BY id, nrings
                                    HAVING nrings > COUNT(id)
                                    ) a
                                WHERE t.id = a.id;"""

    cur.execute(sql_update_ifs)
    conn.commit()

    ##  test construction remove holes
    # print(f"DELETING pre_django.indrz_interiorfloorsection_{floor}")
    # del_floorsection = F"""DELETE FROM pre_django.indrz_interiorfloorsection_{floor} CASCADE
    #                         WHERE tags[1] = '{table.stem}'"""
    # cur.execute(del_floorsection)

    # remove holes in construction areas caused by dxf  symbols
    # print(f"removing holes in CONSTRUCTION AREAS {table.stem}")
    # sql_update_ifs = f"""UPDATE django.buildings_interiorfloorsection t
    #                             SET geom = a.geom
    #                             FROM (
    #                                 SELECT id, ST_Collect(ST_MakePolygon(geom)) AS geom
    #                                 FROM (
    #                                     SELECT id, ST_NRings(geom) AS nrings,
    #                                         ST_ExteriorRing((ST_Dump(geom)).geom) AS geom
    #                                     FROM django.buildings_interiorfloorsection
    #                                     WHERE ST_NRings(geom) > 1
    #                                     ) s
    #                                 GROUP BY id, nrings
    #                                 HAVING nrings > COUNT(id)
    #                                 ) a
    #                             WHERE t.id = a.id;"""
    #
    # cur.execute(sql_update_ifs)


def insert_cartolines(table, dbschema='pre_django'):
    ###  INSERT CARTOLINES #######
    floor = table.stem.split('_')[-1]
    building_name = table.stem.split('_')[1]
    floor_name = floor.lower()
    floor_num = get_floor_float(floor)
    default_floor_id = 92

    dest_table_name_lines = f"indrz_lines_{floor}"

    print(f"inserting DJ CARTOLINES {table.stem}")
    sql_insert_cartolines = f"""INSERT INTO django.buildings_buildingfloorplanline (floor_name, tags, long_name, floor_num,
                                 geom, fk_building_floor_id, fk_building_id)
                                SELECT '{floor}', tags, long_name, {floor_num}, 
                                st_setsrid(st_transform(geom,3857), 3857), 
                        (select id from django.buildings_buildingfloor where floor_num = {floor_num} 
                                and fk_building_id = (select id from django.buildings_building where name = '{building_name}')  ) as fk_building_floor_id,
                        (select id from django.buildings_building where name = '{building_name}') as fk_building_id
                                 FROM {dbschema}.{dest_table_name_lines}
                                 WHERE split_part(tags[1], ',',1) = '{table.stem}'
                                 AND ST_GeometryType(geom)='ST_MultiLineString';
                 """
    cur.execute(sql_insert_cartolines)
    conn.commit()


def set_building_code(dwg_building_code):
    """
    dwg_building_code is the code in the dwg file name for each building
    Uni system actually used a different code for buildings in the DB and search


    """

    for code in building_code_map:
        if code['dwg_building_code'] == dwg_building_code:
            return code['building_code']


def extract_roomcodes(dxf_files):
    for d_file in dxf_files:

        dxf_file = Path(d_file)

        fl_name = dxf_file.stem.split('_')[-1]
        floor_name = fl_name.lower()
        floor_float = get_floor_float(floor_name)
        building_abr = dxf_file.stem.split('_')[1]
        floor_abr = get_floor_str(fl_name)  # ug01 = U1,  eg=EG


        print(f"DELETING pre_django.indrz_labels_{floor_name}")
        sql_del_labels = f"""DELETE FROM pre_django.indrz_labels_{floor_name} CASCADE
                              WHERE split_part(tags[1], ',',1) = '{dxf_file.stem}';"""

        cur.execute(sql_del_labels)
        conn.commit()

        print(f"INSERTING pre_django.indrz_labels_{floor_name}")
        print(f"*************** pre_django.indrz_labels_{building_abr.upper(), floor_abr.upper()}")

        text_where = building_abr.upper() + ".%"

        if building_abr in ('B11', 'B12', 'B13', 'R'):
            text_where = f"""B11a.%' or text like 'B11b.%' or text like 'B11c.%'
            or text like 'B12a.%' or text like 'B12b.%' or text like 'B12c.%'
            or text like 'B13a.%' or text like 'B13b.%' or text like 'B13c.%'
            or text like 'r-%"""

        # campus Zentral, Nord, Sued tract are in one building and one .dxf file
        if building_abr in ('Z', 'S', 'N', 'V', 'L', 'O', 'C'):
            text_where = f"""Z.%' or text like 'S.%'
            or text like 'V.%'
            or text like 'L.%'
            or text like 'O.%'
            or text like 'C.%'
            or text like 'N.%"""

        if building_abr in ('D8', 'D9', 'D10', 'D11', 'D12', 'D13'):
            text_where = f"""D8.%' or text like 'D9.%'
            or text like 'D10.%'
            or text like 'D11.%'
            or text like 'D12.%'
            or text like 'D13.%"""

        normal_case_labels = f"""INSERT INTO pre_django.indrz_labels_{floor_name} (room_code, room_external_id, 
        short_name, long_name, floor_num, floor_name, tags, geom)
        select distinct on (text) text, text as external_id, text as short_name, text as long_name,
            {floor_float}, '{floor_name}', ARRAY['{dxf_file.stem}, {building_abr}'], st_multi(wkb_geometry)  as geom
            FROM dxf_tables.{dxf_file.stem.lower()}
            where st_xmin(wkb_geometry) > 590000
            AND text like '{text_where}';
        """

        cur.execute(f""" UPDATE pre_django.indrz_labels_{floor_name}
        SET room_code = RTRIM(room_code)
        WHERE room_code <> RTRIM(room_code);""")

        cur.execute(normal_case_labels)
        conn.commit()

    return


def table_exists(dxf_file):
    in_db = False
    # t_name = str(dxf_file.stem)
    t_name = dxf_file.split('.')[0]

    sql_table_exists = f"""select exists(select * from information_schema.tables where table_name= '{t_name.lower()}')"""
    cur.execute(sql_table_exists)

    if cur.fetchone()[0]:
        # if true this table exists so do NOT run it
        in_db = True
        return in_db
    else:
        return in_db


def drop_dxf_tables(dxf_files, dbschema='dxf_tables'):
    for dxf_file_name in dxf_files:
        dxf_file = get_dxf_fullpath(dxf_file_name)
        print(f"DROP Table if exits {dbschema}.{dxf_file.stem}")
        sql_drop = F"DROP TABLE IF EXISTS {dbschema}.{dxf_file.stem} CASCADE"
        cur.execute(sql_drop)

        print(f"DROPPING table dxf_tables.{dxf_file.stem}")
        sql_drop_dxf_table = F"DROP TABLE IF EXISTS {dbschema}.{dxf_file.stem} CASCADE"
        cur.execute(sql_drop_dxf_table)

    conn.commit()


def delete_all_campus_data(all_floors, dbschema='pre_django'):
    # delete ALL labels for ENTIRE CAMPUS
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


def delete_db_data(dxf_files: list, campus=None):
    """
    input: dxf_files = list of dxf files
    delete pre_django data for tables labels, lines, spaces, umriss,
    delete django data for tables for buildings_buildingfloorspace,
        buildings_buildingfloorplanline, buildings_interiorfloorsection
    """
    for dxf_file_name in dxf_files:
        dxf_file = get_dxf_fullpath(dxf_file_name)

        print("now deleting db data for ", dxf_file)

        floor_n = dxf_file.stem.split('_')[-1]
        floor = floor_n.lower()

        print(f"DELETING pre_django.indrz_labels_{floor}")
        sql_del_labels = f"""DELETE FROM pre_django.indrz_labels_{floor} CASCADE WHERE split_part(tags[1], ',',1) = '{dxf_file.stem}';"""
        print(sql_del_labels)
        cur.execute(sql_del_labels)
        conn.commit()

        print(f"DELETING pre_django.indrz_LINES_{floor} old pre_django lines in db")
        sql_del_lines = F"DELETE FROM pre_django.indrz_lines_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
        cur.execute(sql_del_lines)
        conn.commit()

        print(f"DELETING pre_django.indrz_SPACES_{floor} old pre_django spaces in db")
        sql_delete_s = F"DELETE FROM pre_django.indrz_spaces_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
        cur.execute(sql_delete_s)
        conn.commit()

        print("DELETING django.buildingfloorspace")
        print("now deleting django.buildings_buildingfloorspace  DJANGO spaces in db")
        del_fspace = F"DELETE FROM django.buildings_buildingfloorspace CASCADE WHERE split_part(tags[1], ',',1) = '{dxf_file.stem}'"
        cur.execute(del_fspace)
        conn.commit()

        print("DELETING django.buildings_buildingfloorplanline  DJANGO cartolines in db")
        del_fplan = F"DELETE FROM django.buildings_buildingfloorplanline CASCADE WHERE split_part(tags[1], ',',1) = '{dxf_file.stem}'"
        cur.execute(del_fplan)
        conn.commit()

        print("DELETING django.buildings_interiorfloorsection DJANGO spaces in db")
        del_floorsection = F"DELETE FROM django.buildings_interiorfloorsection CASCADE WHERE split_part(tags[1], ',',1) = '{dxf_file.stem}'"
        cur.execute(del_floorsection)
        conn.commit()


def import_dxf(dxf_files):
    for dxf_file_name in dxf_files:
        dxf_file = get_dxf_fullpath(dxf_file_name)
        print(f"now running ogr, creating table and importing dxf data {dxf_file_name}")
        dxf2postgis(dxf_file)

def create_pre_django_building(dxf_file_name, building_name, campus=None):
    if not campus:
        return print("Error no campus specified")

    dxf_file = get_dxf_fullpath(dxf_file_name)

    if not building_name:
        # assume building name is the first part of the dxf file name
        building_name = dxf_file.stem.split('_')[1]

    building_name.lower()
    dest_table_name = f"indrz_buildings"

    sql_insert_building = f"""
        WITH existing AS (
        SELECT 1
        FROM pre_django.{dest_table_name}
        WHERE name = '{building_name}'
            )
        INSERT INTO pre_django.{dest_table_name}(name, tags, campus_id, org_id, geom)
            SELECT 
                '{building_name}',
                ARRAY['{dxf_file.stem}','{building_name}'] as tags,
                2 as campus_id,
                1 as org_id,
                st_multi(st_pointonsurface(geom_umriss)) as geom
            FROM (
                SELECT st_buildarea(st_node(geom)) AS geom_umriss
                FROM (
                    SELECT st_union(wkb_geometry) as geom
                    FROM dxf_tables.{dxf_file.stem.lower()}
                    WHERE layer = 'Umriss'
                ) as building_lines
            ) as final_building
            WHERE NOT EXISTS (SELECT 1 FROM existing);
     """
    cur.execute(sql_insert_building)

    conn.commit()

def create_building(building_name, campus_id, org_id):
    if not campus_id or not campus_id or not building_name:
        return print("Error no campus specified")

    dest_table_name = f"buildings_building"

    sql_insert_building = f"""
        WITH existing AS (
        SELECT 1
        FROM django.{dest_table_name}
        WHERE name = '{building_name}'
            )
        INSERT INTO django.{dest_table_name}(name, building_name, campus_id, organization_id, num_floors, geom)
            SELECT 
                '{building_name}',
                '{building_name}',
                {campus_id} as campus_id,
                {org_id} as organization_id,
                1 as num_floors,
                (st_dump(st_transform(geom, 3857))).geom as geom
                FROM pre_django.indrz_buildings 
                 WHERE name = '{building_name}'
                 AND NOT EXISTS (SELECT 1 FROM existing);
     """
    cur.execute(sql_insert_building)
    conn.commit()

def create_pre_django_floor(dxf_file_name, umriss_layer='Umriss'):
    """
    Generate a single umriss or a single floor perimeter polygon
    :param campus:
    :param dxf_file_name:
    :return:
    """
    dxf_file = get_dxf_fullpath(dxf_file_name)

    floor_name = dxf_file.stem.split('_')[-1]
    building_name = dxf_file.stem.split('_')[1]
    floor_num = get_floor_float(floor_name)

    if floor_name.lower() == 'sou':
        floor_name = 'so'

    dest_table_name = f"indrz_umriss_{floor_name.lower()}"

    print(f"DELETING pre_django.{dest_table_name} old pre_django UMRISS in db")
    sql_delete_umriss = F"DELETE FROM pre_django.{dest_table_name} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
    cur.execute(sql_delete_umriss)
    conn.commit()

    # checks if floor exists if exists do nothing
    sql_umriss_new = f"""
    WITH existing AS (
        SELECT 1
        FROM pre_django.{dest_table_name}
        WHERE fk_building_id = (select id from pre_django.indrz_buildings where name = '{building_name}')
        and floor_num = {floor_num}
            )
     INSERT INTO pre_django.{dest_table_name}(short_name, floor_num, tags, fk_building_id, geom)
    select 
    '{floor_name}',
     {floor_num} as floor_num,
     ARRAY['{dxf_file.stem}','{umriss_layer}'] as tags,
     (select id from pre_django.indrz_buildings where name = '{building_name}') as fk_building_floor_id,
     st_multi(geom_umriss_with_holes) as geom
     FROM (SELECT st_buildarea(st_node(geom)) AS geom_umriss_with_holes
           FROM (select st_union(st_forceclosed(wkb_geometry)) as geom  -- forceclosed is needed
                 FROM dxf_tables.{dxf_file.stem}
                 WHERE layer = '{umriss_layer}')
                 as merged_lines)
                     as final_umriss
    WHERE NOT EXISTS (SELECT 1 FROM existing);
     """

    cur.execute(sql_umriss_new)

    conn.commit()

def create_floor(dxf_file_name):
    """
    Generate a single umriss or a single floor perimeter polygon
    :param campus:
    :param dxf_file_name:
    :return:
    """
    dxf_file = get_dxf_fullpath(dxf_file_name)

    floor_name = dxf_file.stem.split('_')[-1]
    building_name = dxf_file.stem.split('_')[1]
    floor_num = get_floor_float(floor_name)

    if floor_name.lower() == 'sou':
        floor_name = 'so'

    src_table_name = f"indrz_umriss_{floor_name.lower()}"

    print(f"DELETING django.buildings_buildingfloor UMRISS in db")
    sql_delete_floor = F"DELETE FROM django.buildings_buildingfloor WHERE tags[1] = '{dxf_file.stem}'"
    cur.execute(sql_delete_floor)
    conn.commit()


    cur.execute(f"""
        WITH existing AS (
            SELECT 1
            FROM django.buildings_buildingfloor
            WHERE floor_num = {floor_num}
                AND fk_building_id = (SELECT id FROM django.buildings_building WHERE name = '{building_name}')
        )
        INSERT INTO django.buildings_buildingfloor (short_name, long_name, name_en, name_de, floor_name, floor_num, geom, fk_building_id, tags)
        SELECT 
            '{floor_name}', 
            '{floor_name}', 
            '{floor_name}',
            '{floor_name}',
            '{floor_name}',
            {floor_num}, 
            st_setsrid(st_transform(u.geom, 3857), 3857) AS geom,
            (SELECT id FROM django.buildings_building WHERE name = '{building_name}') AS fk_building_id, 
            ARRAY['{dxf_file.stem}', '{floor_name}'] AS tags
        FROM pre_django.{src_table_name} AS u
        WHERE u.tags[1] = '{dxf_file.stem}'
        AND NOT EXISTS (SELECT 1 FROM existing);
           """)

    conn.commit()


def insert_umriss(dxf_file_name, umriss_layer, campus=None, new_building=False):
    """
    Generate a single umriss or a single floor perimeter polygon
    :param campus:
    :param dxf_file_name:
    :return:
    """
    dxf_file = get_dxf_fullpath(dxf_file_name)

    floor_name = dxf_file.stem.split('_')[-1]
    floor_num = get_floor_float(floor_name)

    if floor_name.lower() == 'sou':
        floor_name = 'so'

    dest_table_name = f"indrz_umriss_{floor_name.lower()}"

    # building_letters = dxf_file.stem.split('_')[-4]  # 'OD_01_bp_052020'  or  BC_BG_U1_IP_042019

    print(f"DELETING pre_django.{dest_table_name} old pre_django UMRISS in db")
    sql_delete_umriss = F"DELETE FROM pre_django.{dest_table_name} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
    cur.execute(sql_delete_umriss)
    conn.commit()

    sql_umriss_new = f"""
    INSERT INTO pre_django.{dest_table_name}(short_name, floor_num, tags, fk_building_id, geom)
   select 
   '{floor_name}',
    {floor_num} as floor_num,
    ARRAY['{dxf_file.stem}','{umriss_layer}'] as tags,
    1 as fk_building_floor_id,
    st_multi(geom_umriss_with_holes) as geom
    FROM (SELECT st_buildarea(st_node(geom)) AS geom_umriss_with_holes
          FROM (select st_union(st_forceclosed(wkb_geometry)) as geom  -- forceclosed is needed
                FROM dxf_tables.{dxf_file.stem}
                WHERE layer = '{umriss_layer}')
                as merged_lines)
                    as final_umriss;
    """

    cur.execute(sql_umriss_new)

    conn.commit()

    # if new building use insert else update
    if new_building:

        delete_db_data([dxf_file_name])

        print(f"DELETING django.buildings_buildingfloor UMRISS in db")
        sql_delete_floor = F"DELETE FROM django.buildings_buildingfloor WHERE tags[1] = '{dxf_file.stem}'"
        cur.execute(sql_delete_floor)
        conn.commit()


        cur.execute(f"""
            INSERT INTO django.buildings_buildingfloor (short_name, long_name, floor_num, geom,
             fk_building_id, tags)
             SELECT '{floor_name}', '{floor_name}', {floor_num}, st_setsrid(st_transform(u.geom,3857), 3857) as geom,
             2 as fk_building_floor_id, 
             ARRAY['{dxf_file.stem}','{umriss_layer}'] as tags
               FROM pre_django.{dest_table_name} as u
               WHERE u.tags[1] = '{dxf_file.stem}'
               """)

        conn.commit()
    else:
        cur.execute(f"""
            update django.buildings_buildingfloor b set geom = st_setsrid(st_transform(u.geom,3857), 3857)
               FROM pre_django.{dest_table_name} as u
               WHERE u.tags[1] = '{dxf_file.stem}'
               AND b.tags[1] = '{dxf_file.stem}'
               """)

        conn.commit()

    # update building id
    cur.execute(f"""
                update django.buildings_buildingfloor bf set fk_building_id = b.id
                   FROM django.buildings_building as b
                   WHERE st_within(b.geom, bf.geom);
       """)
    conn.commit()


def create_floors(dxf_file_name):
    dxf_file = get_dxf_fullpath(dxf_file_name)
    file_building_name_code = f"{dxf_file.stem.split('_')[1]}"
    building_code = set_building_code(file_building_name_code)

    floor_name = dxf_file.stem.split('_')[-1]
    building_letter = dxf_file.stem.split('_')[1]
    floor_num = get_floor_float(floor_name)


    sql_clean = f"""DELETE from django.buildings_buildingfloor 
                    WHERE tags[1] = '{dxf_file.stem}'"""
    cur.execute(sql_clean)

    building_id = 2

    print(f"inserting buildingfloor {dxf_file.stem}")

    if file_building_name_code in ['B11', 'B12']:

        # this is the original and should be used normally if umriss are in dwg plans
        sql_insert = f"""INSERT INTO django.buildings_buildingfloor (long_name, short_name, floor_num,
                                            geom, fk_building_id, floor_name, tags)
                                    SELECT '{dxf_file.stem}', '{floor_name.upper()}',{floor_num},
                                        st_setsrid(st_transform(geom,3857), 3857),
                                     {building_id}, '{floor_name.upper()}', ARRAY['{dxf_file.stem}',]
                                     FROM pre_django.indrz_umriss_{floor_name}
                                    WHERE tags[1] = '{dxf_file.stem}'"""
    else:
        # no umriss in any dwg plans to create umriss from spaces polyongs using buffer union
        sql_insert = f"""
        INSERT INTO django.buildings_buildingfloor (long_name, short_name, floor_num,
                                            geom, fk_building_id, floor_name, tags)
        SELECT '{dxf_file.stem}', '{floor_name.upper()}', {floor_num}, 
                                        st_multi(st_setsrid(st_transform(ST_Union(ST_Buffer(geom, 0.7, 8)),3857), 3857)),
                                     (select id from django.buildings_building where building_name = '{building_letter}'), '{floor_name.upper()}', ARRAY['{dxf_file.stem}']
                                     FROM pre_django.indrz_spaces_{floor_name}
                                    WHERE tags[1] = '{dxf_file.stem}'
        """


    cur.execute(sql_insert)
    conn.commit()

    # update buildingfloor special_name
    cur.execute("""
        update django.buildings_buildingfloor bf set special_name = b.name, fk_building_id = b.id
           from django.buildings_building as b
           where b.building_name = (regexp_split_to_array(bf.long_name, '_'))[1];""")

    conn.commit()


def clean_up_temp_dxf_server():
    # clean up temp dxf files used for import files on server
    pre_django = ['test', 'test2']
    for campus in pre_django:
        campus_path = f"""/opt/data/media/{campus}"""
        subprocess.call(["rm", "-r", campus_path])


def set_space_type_id(cur):
    # assign all spaces a default value of 94 its like a hard reset of colors all to default light blue
    # this enables geoserver to at least render roomcodes correctly
    ss = "update django.buildings_buildingfloorspace set space_type_id = 94 where 1 = 1;"
    cur.execute(ss)

    sql_isnull = "update django.buildings_buildingfloorspace set space_type_id = 94 where space_type_id IS NULL;"
    cur.execute(sql_isnull)

    print('ASSIGNING SPACE COLORS')
    for type in category_types:
        space_type_name = type['type_name']
        type_id = type['type_code']
        update_space_type_sql = f"""update django.buildings_buildingfloorspace fs set space_type_id = {type_id}
                               from geodata.aau_nightly_data d where d.roomcode = fs.room_code
                               and d.category_de = '{space_type_name}'
                         """

        cur.execute(update_space_type_sql)
        conn.commit()

    for type in room_types:
        space_type_name = type['type_name']
        type_id = type['type_code']

        cur.execute(f"""update django.buildings_buildingfloorspace fs set space_type_id = {type_id}
                               from geodata.aau_nightly_data tc
                               where tc.roomcode = fs.room_code
                                 and tc.fancyname_de like '%{space_type_name}%'; """)

    conn.commit()


def update_sequence():
    sql = """SELECT 'SELECT SETVAL(' ||
       quote_literal(quote_ident(PGT.schemaname) || '.' || quote_ident(S.relname)) ||
       ', COALESCE(MAX(' ||quote_ident(C.attname)|| '), 1) ) FROM ' ||
       quote_ident(PGT.schemaname)|| '.'||quote_ident(T.relname)|| ';'
        FROM pg_class AS S,
             pg_depend AS D,
             pg_class AS T,
             pg_attribute AS C,
             pg_tables AS PGT
        WHERE S.relkind = 'S'
            AND S.oid = D.objid
            AND D.refobjid = T.oid
            AND D.refobjid = C.attrelid
            AND D.refobjsubid = C.attnum
            AND T.relname = PGT.tablename
            AND PGT.tablename != 'public'
            AND PGT.tablename != 'topology'
        ORDER BY S.relname;"""
    cur.execute(sql)

    for q in cur.fetchall():
        cur.execute(q[0])

    sequence_names = """SELECT c.relname AS sequence FROM pg_class c WHERE c.relkind = 'S';"""
    cur.execute(sequence_names)
    for seq in cur.fetchall():
        t = "_"
        if "ogc" in seq[0]:
            x = seq[0].split('_ogc_')[0]
            table_name = x.lower()
            sql = f"select max(ogc_fid) from {table_name}"
            print(table_name)
            cur.execute(sql)
            max_seq_value = cur.fetchone()
            if max_seq_value[0]:
                cur.execute(f"alter sequence {seq[0]} restart with {max_seq_value[0] + 1} ")
        if "_id_seq" in seq[0] and "topol" not in seq[0]:
            x = seq[0].split('_id_')[0]
            table_name = x.lower()
            sql = f"select max(id) from {table_name}"
            print(table_name)
            cur.execute(sql)
            max_seq_value = cur.fetchone()
            if max_seq_value[0]:
                q = f"alter sequence {seq[0]} restart with {max_seq_value[0] + 1} "
                print(q)
                cur.execute(q)
    conn.commit()


def gen_campuses_files(filenames):
    x = []
    for campus_name in campus_names:
        xx = {"name": campus_name, "dxf_files": []}
        list_dxf_files = get_dxf_files(campus_name, only_dxf_names=True)
        for filename in filenames:
            if filename in list_dxf_files:
                xx['dxf_files'].append(filename)
        if xx['dxf_files']:
            x.append(xx)

    print(x)
    return x


def new_ogr_import():
    s = """
    drop table if exists dxf_tables.x3_eg;
    create table dxf_tables.x3_eg
        (
            ogc_fid      serial primary key,
            layer        varchar,
            paperspace   boolean,
            subclasses   varchar,
            linetype     varchar,
            entityhandle varchar,
            text         varchar,
            wkb_geometry geometry(Geometry, 31259)
        );


        create index x3_eg_wkb_geometry_geom_idx
            on dxf_tables.x3_eg using gist (wkb_geometry);


    """

    cur.execute(s)


def do_step_4_floors(dxf_filenames):
    for dxf_filename in dxf_filenames:
        create_floors(dxf_filename)


def newimp(name):
    # new_ogr_import()

    from django.contrib.gis.gdal import DataSource
    from cad_layer_constants import linefeatures
    ds = DataSource(name)
    print("num of layers is ", ds.layer_count)
    lyr = ds[0]
    for feat in lyr:
        # ['Layer', 'SubClasses', 'ExtendedEntity', 'Linetype', 'EntityHandle', 'Text']
        dxf_layer_name = feat.get('Layer')
        dxf_text = feat.get('Text')
        # dxf_ext_entitiy = feat.get('ExtendedEntity')
        # dxf_linetype = feat.get('Linetype')
        # myset.add(dxf_linetype)

        # geom = feat.GetGeometryRef()
        linefeature_layer_names = [name['layer'] for name in linefeatures]

        # if dxf_layer_name in cad_spaces_names:

        try:
            geom_wkt = feat.geom.wkt
        except Exception:
            pass

            # line_geom_types = ['MultiLineString', 'LineString25D', 'LineString', 'MultiLineString25D']
        sql_insert = f"""INSERT INTO dxf_tables.x3_eg (wkb_geometry, text, layer) 
            VALUES (ST_Force2d(ST_MULTI(ST_GeomFromText('{geom_wkt}',31259))), 
            %s,
            %s);"""

        # print("my insert is: ", sql_insert)
        cur.execute(sql_insert, (dxf_text, dxf_layer_name))
    conn.commit()


def run_dxf_updates(dxf_filenames, new_building=False):
    # campus_shorts = ['Kemp', 'Lakeside', 'Stern', 'Musli', 'USI']
    # for file in dxf_filenames:
    #     tmp_file_list = get_dxf_files(filename_filter=campus, only_dxf_names=False)
    #     print("hhmmm", tmp_file_list)
    # tmp_file_list = get_dxf_files(filename_filter='F2', only_dxf_names=False)
    # dxf_filenames.extend(tmp_file_list)

    # STEP 1 if new building do this once
    # if new_building:
    #     logging.info(f"starting new building imported for {dxf_filenames} ")
    #     # STEP 0 remove data otherwise parent child relations will fail ie floor must exist before room
    #     delete_db_data(dxf_filenames)
    #     # STEP 1 remove dxf tables and run ogr2ogr dxf import
    #     drop_dxf_tables(dxf_filenames)
    #     import_dxf(dxf_filenames)
    #     # STEP 2 create pre_django and django tables and data
    #     for dxf_file in dxf_filenames:
    #         d_file = get_dxf_fullpath(dxf_file)
    #         # insert_umriss(d_file, umriss_layer='Umriss', new_building=True)  # pre_django...umriss update
    #     print("now run run_dxf_updates with new_building set to False")
    #     return

    # STEP 1 remove dxf tables and run ogr2ogr dxf import
    # drop_dxf_tables(dxf_filenames)
    # import_dxf(dxf_filenames)

    # STEP 2 ONLY RUN after succesfull import of all dxf files
    # check that all table were succeffully created
    delete_db_data(dxf_filenames)  # delete all temp data in temp tables

    # STEP 3 REQUIRED create space labels
    # inserts into pre_django schema
    extract_roomcodes(dxf_files=dxf_filenames)

    # STEP 4
    # takes from pre_django and inserts into django schema data for each .dxf file
    for dxf_file in dxf_filenames:
        d_file = get_dxf_fullpath(dxf_file)
        # insert_umriss(d_file, umriss_layer='Umriss', new_building=False) # pre_django...umriss update
        insert_spaces(d_file, dxflayername=tuple(cad_spaces_names))
        insert_campus_lines(d_file)
        insert_cartolines(d_file)
        insert_construction(d_file)


def update_floorspace_fields():
    # update django data in spaces table
    cur.execute(f"""
                update django.buildings_buildingfloorspace fs set room_description = tc.fancyname_de, short_name = tc.roomname_de
                                   from geodata.aau_nightly_data tc
                                   where tc.roomcode = room_code;

                update django.buildings_buildingfloorspace fs set long_name = tc.zusatzbezeichnung
                                           from geodata.allrooms2023 tc
                                           where tc.raumnr_schild = room_code
                                            and tc.zusatzbezeichnung is not null;

                update django.buildings_buildingfloorspace fs set fk_building_id = 7
                   WHERE fs.room_code like 'N.%';
                update django.buildings_buildingfloorspace fs set fk_building_id = 6
                   WHERE fs.room_code like 'V.%';
                update django.buildings_buildingfloorspace fs set fk_building_id = 2
                   WHERE fs.room_code like 'S.%';
                update django.buildings_buildingfloorspace fs set fk_building_id = 3
                   WHERE fs.room_code like 'L.%';
                update django.buildings_buildingfloorspace fs set fk_building_id = 8
                   WHERE fs.room_code like 'Z.%';
                update django.buildings_buildingfloorspace fs set fk_building_id = 4
                    WHERE fs.room_code like 'O.%';
                update django.buildings_buildingfloorspace fs set fk_building_id = 5
                    WHERE fs.room_code like 'U.%';
                update django.buildings_buildingfloorspace fs set fk_building_id = 28
                    WHERE fs.room_code like 'UC.%';

                update django.buildings_buildingfloorspace fs set long_name = an.fancyname_de
                                           from geodata.aau_nightly_data an
                                           where an.roomcode = room_code
                                           and an.fancyname_de like '%HS%';

            """)

    sql_space_fields = """
        update django.buildings_buildingfloorspace set room_description = NULL where room_code = room_description;
        update django.buildings_buildingfloorspace set  short_name = NULL where room_code = short_name;
        update django.buildings_buildingfloorspace set  long_name = NULL where room_code = long_name;
    """
    cur.execute(sql_space_fields)
    conn.commit()

def night_data_sync():
    """
    syncs data from aau campus api to local db
    """
    rooms = AauRoomsApi().get_all_rooms()

    if rooms:
        logging.info("yes data from AAU api rooms available")
    else:
        logging.info("no room data provided by AAU api")

    cur.execute("TRUNCATE geodata.aau_nightly_data RESTART IDENTITY;")
    for room in rooms:
        buildingname = room['buildingname']
        buildingcolor = room['buildingcolor']
        category_de = room['category_de']
        category_en = room['category_en']
        fancyname_de = room['fancyname_de']
        fancyname_en = room['fancyname_en']
        floorname = room['floorname']
        pk_big = room['pk_big']
        roomcode = room['roomcode']
        roomname_de = room['roomname_de']
        roomname_en = room['roomname_en']
        capacity = room['capacity']
        tid = room['tid']

        insert_q = """insert into geodata.aau_nightly_data (building_name, building_color, category_de,
         category_en, fancyname_de, fancyname_en, floorname, pk_big, roomcode, roomname_de, roomname_en, capacity, tid)
         values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        rec_to_insert = (buildingname, buildingcolor,
                         category_de,
                         category_en,
                         fancyname_de,
                         fancyname_en,
                         floorname,
                         pk_big,
                         roomcode,
                         roomname_de,
                         roomname_en,
                         capacity,
                         tid)
        cur.execute(insert_q, rec_to_insert)
        conn.commit()

        bg_sq = """
        update geodata.aau_nightly_data set fancyname_de = roomcode where roomcode like 'HS %';

        update geodata.aau_nightly_data set roomcode = ar.raumnr
                from geodata.allrooms2023 ar
                where ar.raumnr_schild = roomcode and ar.raumnr_schild like 'HS %';
        
        update geodata.aau_nightly_data set fancyname_de = roomname_de where fancyname_de is null;
        
        update geodata.aau_nightly_data set fancyname_en = roomcode  where fancyname_de like 'B11a%' or fancyname_de like 'B11b%' or fancyname_de like 'B11c%';
        update geodata.aau_nightly_data set roomcode = fancyname_de  where fancyname_de like 'B11a%' or fancyname_de like 'B11b%' or fancyname_de like 'B11c%';
        update geodata.aau_nightly_data set fancyname_de = fancyname_en  where roomcode like 'B11a%' or fancyname_de like 'B11b%' or fancyname_de like 'B11c%';
        
        update geodata.aau_nightly_data set roomcode = 'S.0.26'  where roomcode = 'E.0.26'; -- HS A
        update geodata.aau_nightly_data set roomcode = 'S.0.22'  where roomcode = 'E.0.22'; -- HS B
        update geodata.aau_nightly_data set roomcode = 'S.0.34'  where roomcode = 'E.0.34'; -- HS C
        
        """
        cur.execute(bg_sq)

        conn.commit()


if __name__ == '__main__':
    conn = psycopg2.connect(con_dj_string)
    cur = conn.cursor()

    # This file runs nightly every day in a cronjob
    # STEP 2 import dxf
    # Run this as nightly cron job
    time_in_hrs = 24
    time_in_days = time_in_hrs/24 # convert hurs to days float
    # files = new_dxf_files(days=time_in_days)
    files = ['Lakeside_B01_EG.dxf',]
    logging.info(f"running nightly dxf sync on files {files}")

    # uncomment to run bigger import of files
    # campus_shorts = ['Kemp', 'Lakeside', 'Stern', 'Musli', 'USI', 'Mensa', 'Campus', 'Stiftungsgebaeude_O', 'USI_U']
    # import ALL dxf files
    # for name in building_code_map:
    #     tmp_file_list = get_dxf_files(filename_filter=name['dwg_building_code'], only_dxf_names=False)
    #     dxf_filenames.extend(tmp_file_list)

    # files = get_dxf_files(filename_filter='Campus_Z_S_L_N_V_OG02', only_dxf_names=False)
    # logging.info(f"one off file import {files}")

    # uncomment to run individual file import
    # files = ['Campus_Z_S_L_N_V_OG01.dxf', ]

    if files:
        logging.info(f"import dxf files: {files}")

        # STEP 1 remove dxf tables and run ogr2ogr dxf import
        drop_dxf_tables(files)
        import_dxf(files)

        # STEP 1.1 IF NEW BUILDING
        # create the building, then import the individual floor plans
        # create_pre_django_building(files[0], 'B01', campus=2)
        # create_building(building_name='B01', campus_id=2, org_id=1)

        # STEP 2 ONLY RUN after succesfull import of all dxf files
        # check that all table were succeffully created
        delete_db_data(files)  # delete all temp data in temp tables

        # STEP 3 REQUIRED create space labels
        # inserts into pre_django schema
        extract_roomcodes(dxf_files=files)

        # STEP 3.1 Re-create floor
        create_pre_django_floor(files[0], umriss_layer='Umriss')
        create_floor(files[0])

        # STEP 4
        # takes from pre_django and inserts into django schema data for each .dxf file
        for dxf_file in files:
            d_file = get_dxf_fullpath(dxf_file)
            # insert_umriss(d_file, umriss_layer='Umriss', new_building=False) # pre_django...umriss update
            insert_spaces(d_file, dxflayername=tuple(cad_spaces_names))
            insert_campus_lines(d_file)
            insert_cartolines(d_file)
            insert_construction(d_file)

        # clean_geoms()  # remove eroneous geom

        logging.info(f"DONE dxf import")
    else:
        logging.info(f"NO dxf files to import")

    # get all rooms from aau api and import to db per night
    # night_data_sync()
    # update_floorspace_fields()
    # import_capacity()  # udpate space  capacity
    # set_space_type_id(cur)
    # special_room_import_rule(cur, conn)
    # logging.info("night_data_sync done")

    ## end nightly cron job

    conn.close()
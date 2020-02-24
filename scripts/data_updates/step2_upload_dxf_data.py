import pandas as pd
import os
from pathlib import Path, PurePath

import subprocess
import psycopg2

from utils import unique_floor_names, get_floor_float

from indrz_secrets import con_string_navigatur, ogr_db_con_navigatur

conn = psycopg2.connect(con_string_navigatur)
cur = conn.cursor()

linefeatures = [
{'layer': 'A2-TUER-SYM050', 'type': 'door'},
{'layer': 'A_A29_VER', 'type':'outer-wall'},
{'layer': 'E_S29', 'type': 'sink'},
{'layer': 'E_M26', 'type':'chairs'},
{'layer': 'E_X49', 'type': 'miss'},
{'layer': 'S_29', 'type': 'stairs'},
{'layer': 'S__29', 'type': 'stairs'},
{'layer': 'S_27', 'type':'stairs'},
{'layer': 'S_26', 'type':'stairs'},
{'layer': 'S__27', 'type':'stairs'},
{'layer': 'H_L27', 'type':'elevator'},
{'layer': 'OUT26', 'type':'outer-wall'},
{'layer': 'O_F49', 'type': 'window'},
{'layer': 'O_T49', 'type': 'door'},
{'layer': 'O_T29', 'type': 'miss'},
{'layer': 'M_L29', 'type':'inner-wall'},
{'layer': 'M_A26', 'type':'outer-wall'},
{'layer': 'M_A27', 'type':'outer-wall'},
{'layer': 'M_A28', 'type': 'miss'},
{'layer': 'M_A29', 'type':'outer-wall'},
{'layer': 'M_L28', 'type': 'miss'},
{'layer': 'M_Z28', 'type': 'miss'},
{'layer': 'M_Z29', 'type':'inner-wall'},
{'layer': 'M_V29', 'type':'outer-wall'},
{'layer': 'M_V29 (Fassadenverkleidung)', 'type': 'window'},
{'layer': 'Z_010', 'type':'outer-wall'},
{'layer': 'Parkplatz', 'type':'parking'},
{'layer': 'DA26ST', 'type':'dachstuhl'},
{'layer': 'DA27ST', 'type':'dachstuhl'},
{'layer': 'DA29DR', 'type':'dachstuhl'},
{'layer': 'X_S_29', 'type': 'stair'},
{'layer': 'X_S27', 'type': 'stair'},
{'layer': 'X_O_F49', 'type': 'window'},
{'layer': 'X_O_T49', 'type': 'miss'},
{'layer': 'X_H_L27', 'type': 'miss'},
{'layer': 'X_M_A29', 'type': 'miss'},
{'layer': 'X_M_Z29', 'type': 'miss'}
]


cad_layer_names = [x['layer'] for x in linefeatures]
cad_layer_names = tuple(cad_layer_names)

cad_spaces_names = 'Z_009'
cad_label_layers = ['B_127N', 'B_227Z','XRNR0', 'XRNR', 'GUT_RAUMSTEMPEL']
cad_umriss = ['B_227IDTR', 'A_A29_VER', 'O_F49', 'M_A29',]
cad_umriss_layers = tuple(cad_umriss)
cad_missing_stairs_elevators = ['X_S_29', 'X_S27', 'X_O_F49', 'X_O_T49', 'X_H_L27', 'X_M_A29','X_M_Z29',]
cad_missing = tuple(cad_missing_stairs_elevators)

# FILE_DIR = 'c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/campus-updates/'
FILE_DIR = 'c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/'

# TODO add S__27  missing from lines DE-U1


def assign_space_type():
    set_null = """UPDATE django.buildings_buildingfloorspace set space_type_id = 94
                                WHERE space_type_id ISNULL; """

    cur.execute(set_null)
    conn.commit()

    space_type_map = {"Büro": 63, "WC": 91, "wc h": 104, "wc her": 104, "wc d": 105, "wc dam": 105,
                      "wc wheel": 106, "wc beh": 106, "stieg": 79, "aufz": 33, "sth": 79,
                      "sekret": 103, "ramp": 108, "aula": 4, "labor": 50, "lift": 33, "gang": 44}

    for k, v in space_type_map.items():

        sql_update_spacetype = f"""UPDATE django.buildings_buildingfloorspace set space_type_id = {v} 
                                    WHERE upper(room_description) LIKE upper('%{k}%');"""


        print(sql_update_spacetype)
        cur.execute(sql_update_spacetype)
        conn.commit()

    type_ids = [#{'type_id': 44, 'color': '#FFF8CF'},  # Flure, Hallen, Aula, Gang, Stiege
                # {'type_id': 91, 'color': '#9D9D9D'},  # WC
                {'type_id': 20, 'color': '#F5D0A8'},  # Student Zones, edv raueme pc raum, gemeinschafts raum
                {'type_id': 22, 'color': '#CD81A8'},  # versammlungsraueme Festsaal
                {'type_id': 103, 'color': '#4DC7FF'},  # Sekretariat  Office admin
                {'type_id': 6, 'color': '#006699'},  # unterrichts raume übungs raume Seminar Hörsaal
                ]

    for type in type_ids:
        color = type['color']
        type_id = type['type_id']
        sql_update_color = f"""update django.buildings_buildingfloorspace as d set space_type_id = {type_id} 
                     FROM geodata.tu_data AS a
                     WHERE d.room_code = a.room_code
                     AND a.color = '{color}';"""

        cur.execute(sql_update_color)
        conn.commit()


def clean_geoms():
    remove_big_poly = """Delete from django.buildings_buildingfloorspace 
                WHERE room_code ='OC01N24' AND room_description = 'LAGER';"""
    cur.execute(remove_big_poly)

    remove_long_planlines = """delete from django.buildings_buildingfloorplanline where st_length(geom)>1000;"""
    cur.execute(remove_long_planlines)

    remove_short_planlines = """delete from django.buildings_buildingfloorplanline where st_length(geom) < 0.001"""
    cur.execute(remove_short_planlines)

    remove_large_room = """delete from django.buildings_buildingfloorspace where st_area(geom) > 4500"""
    cur.execute(remove_large_room)

    conn.commit()


def get_dxf_files(base_dir, campus, floor=None, name_only=False):

    dxf_dir_path = Path(base_dir + campus)
    dxf_list = os.listdir(dxf_dir_path)
    dxf_files = []
    for dxf in dxf_list:
        if PurePath(dxf).suffix == ".dxf":
                dxf_files.append(dxf)

    if name_only:
        return dxf_files

    dxf_file_paths = []
    for dxf in dxf_files:
        p = Path.joinpath(dxf_dir_path, dxf)
        if floor:
            if p.stem.split('_')[1] == floor:
                dxf_file_paths.append(p)
        else:
            dxf_file_paths.append(p)

    return dxf_file_paths


def get_dxf_fullpath(base_dir, campus, dxf_file_name):
    dxf_dir_path = Path(base_dir + campus)

    dxf_file_full_path = Path.joinpath(dxf_dir_path, dxf_file_name)

    return dxf_file_full_path


def dxf2postgis(dxf_file, campus_name):

    table_name = str(dxf_file.stem)

    print(f"now importing via ogr2ogr , {table_name.lower()}")

    # subprocess.run([
    #     "ogr2ogr", "-a_srs", "EPSG:31259",
    #     "-nlt", "PROMOTE_TO_MULTI",
    #     "-lco", "OVERWRITE=YES",
    #     "-lco", f"SCHEMA={campus_name.lower()}", "-skipfailures", "-f", "PostgreSQL", ogr_db_con_navigatur,
    #     "-nln", table_name.lower(), str(dxf_file)])


    subprocess.run([
        "ogr2ogr", "-a_srs", "EPSG:31259", "-oo", "DXF_FEATURE_LIMIT_PER_BLOCK=-1",
        "-nlt", "PROMOTE_TO_MULTI", "-oo", "DXF_INLINE_BLOCKS=FALSE", "-oo", "DXF_MERGE_BLOCK_GEOMETRIES=False",
        "-lco", "OVERWRITE=YES",
        "-lco", f"SCHEMA={campus_name.lower()}", "-skipfailures", "-f", "PostgreSQL", ogr_db_con_navigatur,
        "-nln", table_name.lower(), str(dxf_file)])

    print("DONE running ogr2ogr")



def get_csv_fullpath(base_dir, campus, dxf_file_name):
    dxf_dir_path = Path(base_dir + campus )

    dxf_file_full_path = Path.joinpath(dxf_dir_path, dxf_file_name)

    return dxf_file_full_path



def insert_spaces_cartolines(campus, table):
    floor = table.stem.split('_')[-3]
    floor_num = get_floor_float(floor)
    dest_table_name_spaces = f"indrz_spaces_{floor}"
    dest_table_name_lines = f"indrz_lines_{floor}"


    print(f"inserting lines {table.stem}")

    sql_lines = f"""INSERT INTO campuses.{dest_table_name_lines}( long_name, tags, geom)
                        SELECT layer, ARRAY['{table.stem}', layer], wkb_geometry
                        FROM {campus.lower()}.{table.stem}
                        WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                        AND layer in {cad_layer_names}"""
    cur.execute(sql_lines)
    conn.commit()


    print(f"inserting campuses spaces {table.stem}")

    sql_spaces = f"""INSERT INTO campuses.{dest_table_name_spaces}(long_name, tags, geom)
                    SELECT layer, ARRAY['{table.stem}', layer], st_multi(st_buildarea(wkb_geometry))
                FROM {campus.lower()}.{table.stem}
                WHERE ST_NPoints(wkb_geometry) >= 4
                AND layer in ('{cad_spaces_names}')"""
    cur.execute(sql_spaces)
    conn.commit()

    ###  INSERT CARTOLINES #######
    print(f"inserting DJ CARTOLINES {table.stem}")
    sql_insert_cartolines = f"""INSERT INTO django.buildings_buildingfloorplanline (floor_name, tags, long_name, floor_num,
                                 geom, fk_building_floor_id)
                                SELECT '{floor}', tags, long_name, {floor_num}, st_setsrid(st_transform(geom,3857), 3857), 1
                                 FROM campuses.{dest_table_name_lines}
                                 WHERE split_part(tags[1], ',',1) = '{table.stem}'
                                 AND ST_GeometryType(geom)='ST_MultiLineString'

                 """


    print(sql_insert_cartolines)
    cur.execute(sql_insert_cartolines)
    conn.commit()

    ###  INSERT SPACES #######

    print(f"inserting DJ SPACES {table.stem}")

    sql_dj_spaces = f"""INSERT INTO django.buildings_buildingfloorspace(long_name, tags, geom, floor_num, floor_name, fk_building_floor_id)
                        SELECT layer, ARRAY['{table.stem}', layer], st_setsrid(st_multi(st_buildarea(st_transform(wkb_geometry, 3857))), 3857),
                            {floor_num}, '{floor}', 1
                FROM {campus.lower()}.{table.stem} 
                WHERE ST_NPoints(wkb_geometry) >= 4
                AND layer in ('{cad_spaces_names}')"""

    # OLD QUERY was not importing all generated polys why ?  not sure
    # sql_insert_spaces = f"""INSERT INTO django.buildings_buildingfloorspace (long_name, floor_num, floor_name, tags, geom,
    #                             fk_building_floor_id )
    #                         SELECT long_name, {floor_num}, '{floor}', tags, st_setsrid(st_transform(geom,3857), 3857), 1
    #                         FROM campuses.{dest_table_name_spaces}
    #                         WHERE split_part(tags[1], ',',1) = '{table.stem}'
    #              """

    print(sql_dj_spaces)
    cur.execute(sql_dj_spaces)
    conn.commit()


def step1_import_csv_roomcodes(base_dir, campus, dxf_files):

    for dxf_file in dxf_files:
        dxf_file = get_dxf_fullpath(base_dir, campus + "/", dxf_file)
        csv_filename = dxf_file.stem + "_roomcodes.csv"
        csv_file = get_csv_fullpath(base_dir, campus + "/", csv_filename)

        floor_name = dxf_file.stem.split('_')[-3]
        floor_num = get_floor_float(floor_name)

        df = pd.read_csv(csv_file, delimiter=",", error_bad_lines=False)

        # print(df.columns)
        # print(df.count)
        # remove all rows where x coord is null
        df = df[df['Position X'].notnull()]

        # print(df.count)
        # remove all rows where x coord is invalid like 43.23
        df = df[df['Position X'] > 700000]

        # print(df.count)

        for index, row in df.iterrows():
            cad_layer = row['Layer']
            x = row['Position X']
            y = row['Position Y']
            room_des = row['RAUMBEZEICHNUNG']
            room_n = row['RAUMNUMMER']  # this is used as the roomcode but has spaces must remove all
            roomcode = str(room_n).replace(" ", "")

            geom_sql = f"st_multi(ST_SetSRID(ST_MakePoint({x}, {y}), 31259))"

            if roomcode != 'nan':

                sql = f"""INSERT INTO campuses.indrz_labels_{floor_name.lower()} (short_name, long_name,
                            floor_num, floor_name, room_code, tags, geom)
                            VALUES ('{room_n}', '{room_des}', {floor_num},'{floor_name}',
                                  '{roomcode}', ARRAY['{dxf_file.stem}, {campus.lower()}'], {geom_sql});
                                 """

                print(sql)
                cur.execute(sql)
                conn.commit()

                s2alter = f"""alter table campuses.indrz_labels_{floor_name.lower()} owner to tu; """
                cur.execute(s2alter)
                conn.commit()

        print("ASSIGNING roomcode and room description to spaces from csv points")

        s = f"""Update django.buildings_buildingfloorspace AS s
                SET room_code = pt.room_code, room_description = pt.long_name
                FROM campuses.indrz_labels_{floor_name.lower()} AS pt
                WHERE st_contains(s.geom, st_transform(pt.geom, 3857))
                AND s.floor_name = '{floor_name}';"""

        cur.execute(s)
        conn.commit()


def reimport_dxf(base_dir, campus, dxf_files, re_import=False):

    for dxf_file_name in dxf_files:

        # dxf_file = get_dxf_fullpath(campus, dxf_file_name)
        dxf_file = get_dxf_fullpath(base_dir, campus + "/", dxf_file_name)

        print(dxf_file)

        floor = dxf_file.stem.split('_')[-3]

        if re_import:
            # remove data generated by function step1_import_csv_roomcodes
            print("now removing old points   spaces in db")
            sql_delete_labels = F"DELETE FROM campuses.indrz_labels_{floor.lower()} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
            print(sql_delete_labels)
            cur.execute(sql_delete_labels)
            conn.commit()


            print(f"now droping table {campus.lower()}.{dxf_file.stem}")
            sql_drop = F"DROP TABLE IF EXISTS {campus.lower()}.{dxf_file.stem} CASCADE"
            cur.execute(sql_drop)
            conn.commit()

            print(f"now removing  campuses.indrz_lines_{floor} old campuses lines in db")
            sql_delete = F"DELETE FROM campuses.indrz_lines_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
            cur.execute(sql_delete)
            conn.commit()

            print(f"now removing campuses.indrz_lines_{floor} old campuses spaces in db")
            sql_delete_s = F"DELETE FROM campuses.indrz_spaces_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
            print(sql_delete_s)
            cur.execute(sql_delete_s)
            conn.commit()

            print("deleting spaces and cartolines in DJANGO schema")

            print("now deleting django.buildings_buildingfloorspace  DJANGO spaces in db")
            sql_delete = F"DELETE FROM django.buildings_buildingfloorspace CASCADE WHERE split_part(tags[1], ',',1) = '{dxf_file.stem}'"
            cur.execute(sql_delete)
            conn.commit()

            print("now deleting django.buildings_buildingfloorplanline  DJANGO cartolines in db")
            sql_delete = F"DELETE FROM django.buildings_buildingfloorplanline CASCADE WHERE split_part(tags[1], ',',1) = '{dxf_file.stem}'"
            cur.execute(sql_delete)
            conn.commit()

        print(f"now running ogr, creating table and importing dxf data {dxf_file.stem}")
        dxf2postgis(dxf_file, campus)

        print("DONE Generating table")
        print(f"now inserting to lines and spaces into db  table called {dxf_file.stem}")
        insert_spaces_cartolines(campus, dxf_file)


if __name__ == '__main__':
    path_src_dir = 'c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/'
    path_src_local = 'c:/Users/mdiener/ownCloud/Shared/NavigaTUr/'
    path_src_dir_server = "/opt/src_indrz/indrz-tu/data/indrz/"
    path_src_dir_med = "/opt/data/media/"

    # reimport_dxf('Karlsplatz', ['AA_AB_AC_AD_AE_AF_AG_AI_EG_IP_112018.dxf'], re_import=True)
    # reimport_dxf('Getreidemarkt', ['BA_01_IP_032019.dxf'], re_import=True)
    # step1_import_csv_roomcodes('Getreidemarkt', ['BA_01_IP_032019.dxf'])
    # reimport_dxf('Getreidemarkt', ['BH_01_IP_042019.dxf'], re_import=True)
    # step1_import_csv_roomcodes('Getreidemarkt', ['BH_01_IP_042019.dxf'])
    # reimport_dxf('Getreidemarkt', ['BA_04_IP_032019.dxf'], re_import=True)
    # step1_import_csv_roomcodes('Getreidemarkt', ['BA_04_IP_032019.dxf'])

    # step1_import_csv_roomcodes('Karlsplatz', ['AA_AB_AC_AD_AE_AF_AG_AI_EG_IP_112018.dxf'] )
    # reimport_dxf('Karlsplatz', get_dxf_files('Karlsplatz', name_only=True), re_import=True)
    # step1_import_csv_roomcodes('Karlsplatz', get_dxf_files('Karlsplatz', name_only=True))


    # print("DONE")

    # import all dxf files in a directory

##########################################################
    ########### kill all these since names are wrong #############
    ## done on  31.01.2020  ####
    # guss_list = ['CF_01_CG_02_IP_042019.dxf',
    #                 'CF_02_CG_03_IP_042019.dxf',
    #                 'CF_03_CG_05_IP_042019.dxf',
    #                 'CF_04_CG_06_IP_042019.dxf',
    #                 'CF_EG_CG_01_IP_042019.dxf',
    #                 'CF_SOU_CG_EG_IP_042019.dxf',
    #                 'CF_U1_CG_U1_IP_042019.dxf',
    #                 'CF_Z2_CG_04_IP_042019.dxf',
    #                 'GA_EG_IP_042019.dxf',
    #                 'GA_U1_U2_IP_042019.dxf'
    #              ]
    # reimport_dxf(path_src_dir_med, 'Gusshaus', guss_list, re_import=True)
    # step1_import_csv_roomcodes(path_src_dir_med, 'Gusshaus', guss_list)

#################################################

    ##   one off 31.01.2020  removed

    # getreid_new_list = ['BD_BE_04_IP_042019.dxf',
    #                     'BD_BE_05_IP_042019.dxf',
    #                     'BD_BE_06_IP_042019.dxf',
    #                     'BD_BE_07_DG_IP_042019.dxf',
    #                     'QA_EG_ZE_IP_15072019.dxf',
    #                     ]
    # reimport_dxf(path_src_dir_med, 'Getreidemarkt', getreid_new_list, re_import=True)
    # step1_import_csv_roomcodes(path_src_dir_med, 'Getreidemarkt', getreid_new_list)

    ############################################################################


    # campus_name = 'Freihaus'
    #
    # list_dxf_files = get_dxf_files(base_dir=path_src_dir_med, campus=campus_name, name_only=True)
    # reimport_dxf(base_dir=path_src_dir_med, campus=campus_name, dxf_files=list_dxf_files, re_import=True)
    # step1_import_csv_roomcodes(base_dir=path_src_dir_med, campus=campus_name, dxf_files=list_dxf_files)


    campuses = ['Getreidemarkt', 'Freihaus', 'Karlsplatz', 'Gusshaus', 'Arsenal']


    for campus_name in campuses:
        list_dxf_files = get_dxf_files(base_dir=path_src_dir_med, campus=campus_name, name_only=True)
        reimport_dxf(base_dir=path_src_dir_med, campus=campus_name, dxf_files=list_dxf_files, re_import=True)
        step1_import_csv_roomcodes(base_dir=path_src_dir_med, campus=campus_name, dxf_files=list_dxf_files)


    # print(len(get_dxf_files('Karlsplatz', name_only=True)))

    # reimport_dxf(path_src_dir_med, 'Arsenal', ['OA_EG_IP_032019.dxf'], re_import=True)
    # step1_import_csv_roomcodes(path_src_dir_med, 'Arsenal', ['OA_EG_IP_032019.dxf'])


    # reimport_dxf(path_src_local, 'Karlsplatz', ['AA_AB_AC_AD_AE_AF_AG_AI_ZU_ZE_IP_112018.dxf'], re_import=True)
    # step1_import_csv_roomcodes(path_src_local, 'Karlsplatz', ['AA_AB_AC_AD_AE_AF_AG_AI_ZU_ZE_IP_112018.dxf'] )


    assign_space_type()
    clean_geoms()

    # clean up temp dxf files used for import files on server
    for campus in campuses:
        campus_path = f"""/opt/data/media/{campus}"""
        subprocess.call(["rm", "-r", campus_path])

    conn.close()

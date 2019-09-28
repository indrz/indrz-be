import pandas as pd
import os
from pathlib import Path, PurePath

import subprocess
import psycopg2

from utils import unique_floor_names, con_string, ogr_db_con

conn = psycopg2.connect(con_string)
cur = conn.cursor()

linefeatures = [
{'layer': 'E_S29', 'type': 'sink'},
{'layer': 'O_F49', 'type': 'window'},
{'layer': 'M_V29 (Fassadenverkleidung)', 'type': 'window'},
{'layer': 'S_29', 'type': 'stairs'},
{'layer': 'S__29', 'type': 'stairs'},
{'layer': 'S_27', 'type':'stairs'},
{'layer': 'S__27', 'type':'stairs'},
{'layer': 'X_S_29', 'type':'stairs'},
{'layer': 'E_M26', 'type':'chairs'},
{'layer': 'H_L27', 'type':'elevator'},
{'layer': 'M_A29', 'type':'outer-wall'},
{'layer': 'A_A29_VER', 'type':'outer-wall'},
{'layer': 'OUT26', 'type':'outer-wall'},
{'layer': 'M_L29', 'type':'inner-wall'},
{'layer': 'M_Z29', 'type':'inner-wall'},
{'layer': 'A2-TUER-SYM050', 'type': 'door'},
{'layer': 'O_T49', 'type': 'door'},
{'layer': 'O_T29', 'type': 'door'}]

cad_layer_names = [x['layer'] for x in linefeatures]
cad_layer_names = tuple(cad_layer_names)

cad_spaces_names = 'Z_009'
cad_label_layers = ['B_127N', 'B_227Z','XRNR0', 'XRNR', 'GUT_RAUMSTEMPEL']
cad_umriss = ['B_227IDTR', 'A_A29_VER', 'O_F49', 'M_A29',]
cad_umriss_layers = tuple(cad_umriss)
cad_missing_stairs_elevators = ['X_S_29', 'X_S27', 'X_O_F49', 'X_O_T49', 'X_H_L27', 'X_M_A29','X_M_Z29',]
cad_missing = tuple(cad_missing_stairs_elevators)

# TODO add S__27  missing from lines DE-U1

def get_dxf_fullpath(campus, dxf_file_name):
    dxf_dir_path = Path('c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/' + campus + '/dxf')

    dxf_file_full_path = Path.joinpath(dxf_dir_path, dxf_file_name)

    return dxf_file_full_path


def get_dxf_files(campus_name, floor=None, only_dxf_names=False):

    dxf_dir_path = Path('c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/' + campus_name + '/dxf')
    dxf_list = os.listdir(dxf_dir_path)
    dxf_files = []
    for dxf in dxf_list:
        if PurePath(dxf).suffix == ".dxf":
                dxf_files.append(dxf)
    #print(len(dxf_files))

    dxf_file_paths = []

    if only_dxf_names:
        return dxf_files

    for dxf in dxf_files:
        p = Path.joinpath(dxf_dir_path, dxf)
        if floor:
            if p.stem.split('_')[1] == floor:
                dxf_file_paths.append(p)
        else:
            dxf_file_paths.append(p)

    return dxf_file_paths


def table_exists(dxf_file):
    in_db = False
    t_name = str(dxf_file.stem)

    sql_table_exists = f"""select exists(select * from information_schema.tables where table_name={t_name})"""
    cur.execute(sql_table_exists)

    if cur.fetchone()[0]:
        # if true this table exists so do NOT run it
        in_db = True
        return in_db
    else:
        return in_db


def dxf2postgis(dxf_file, campus_name):

    table_name = str(dxf_file.stem)

    print(f"now importing , {table_name}")

    subprocess.run([
        "ogr2ogr", "-a_srs", "EPSG:31259", "-oo", "DXF_FEATURE_LIMIT_PER_BLOCK=-1",
        "-nlt", "PROMOTE_TO_MULTI", "-oo", "DXF_INLINE_BLOCKS=FALSE", "-oo", "DXF_MERGE_BLOCK_GEOMETRIES=False",
        "-lco", f"SCHEMA={campus_name.lower()}", "-skipfailures", "-f", "PostgreSQL", ogr_db_con, "-nln", table_name, str(dxf_file)])


def step1_import_all_dxf_to_working(campus):
    dxf_file_paths = get_dxf_files(campus)
    for dxf_file in dxf_file_paths:
        dxf2postgis(dxf_file, campus)


# RUN STEP 1 for ALL dxf files OR run import_dxf() to import specific list of dxf files


def step2_insert_lines_into_floor_tables(campus):
    # assume all tables already exist if not
    # create using create_tables.py  create_empty_tables()
    # it will generate empty tables to insert into

    table_names = get_dxf_files(campus)

    for table in table_names:
        floor = table.stem.split('_')[-3]
        dest_table_name = f"indrz_lines_{floor}"

        sql = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) SELECT layer, ARRAY['{table.stem}', layer], wkb_geometry 
                    FROM {campus.lower()}.{table.stem} 
                    WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                    AND layer in {cad_layer_names}"""
        print(f"now inserting, {table.stem}")
        cur.execute(sql)
        conn.commit()


def step3_insert_spaces_into_floor_tables(campus):
    # assume all tables already exist if not
    # create using create_tables.py script
    # it will generte empty tables to insert into

    table_names = get_dxf_files(campus)

    for table in table_names:
        floor = table.stem.split('_')[-3]
        dest_table_name = f"indrz_spaces_{floor}"

        print(f"now importing {table.stem}")

        sql = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) SELECT layer, ARRAY['{table.stem}', layer], st_multi(st_buildarea(wkb_geometry))
                    FROM {campus.lower()}.{table.stem} 
                    WHERE ST_NPoints(wkb_geometry) >= 4
                    AND ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                    AND layer in ('{cad_spaces_names}')"""
        cur.execute(sql)
        conn.commit()


def insert_missing_cad_layer(campus, trak, cad_layer_name, remove=False,insert=False):
    """ select data from a specific cad layer and insert into our db """

    table_names = get_dxf_files(campus)

    for table in table_names:
        sql = ""

        floor = table.stem.split('_')[-3]
        dest_table_name = f"indrz_lines_{floor}"
        n = table.stem.lower()

        if n.startswith(trak):

            if remove:
                sql = f"""DELETE FROM {campus}.{dest_table_name}
                          WHERE layer in ('{cad_layer_name}')"""
            if insert:
                sql = f"""INSERT INTO {campus}.{dest_table_name}(long_name, geom) SELECT layer, wkb_geometry 
                            FROM {campus}.{table.stem} 
                            WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                            AND layer in ('{cad_layer_name}')"""
            print(sql)

            cur.execute(sql)
            conn.commit()


def insert_campuses_all(campus, table, lines=False, spaces=False):
    floor = table.stem.split('_')[-3]

    if lines:
        print(f"inserting lines {table.stem}")
        dest_table_name = f"indrz_lines_{floor}"
        sql_lines = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) SELECT layer, ARRAY['{table.stem}', layer], wkb_geometry 
                    FROM {campus.lower()}.{table.stem} 
                    WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                    AND layer in {cad_layer_names}"""
        cur.execute(sql_lines)
        conn.commit()

    if spaces:
        print(f"inserting spaces {table.stem}")
        dest_table_name = f"indrz_spaces_{floor}"
        sql_spaces = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) SELECT layer, ARRAY['{table.stem}', layer], st_multi(st_buildarea(wkb_geometry))
                    FROM {campus.lower()}.{table.stem} 
                    WHERE ST_NPoints(wkb_geometry) >= 4
                    AND ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                    AND layer in ('{cad_spaces_names}')"""
        cur.execute(sql_spaces)
        conn.commit()


def insert_missing_cadlines(campus, table):
    floor = table.stem.split('_')[-3]

    print(f"inserting lines {table.stem}")
    dest_table_name = f"indrz_lines_{floor}"
    sql_lines = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) 
                SELECT layer, ARRAY['{table.stem}', layer], wkb_geometry 
                FROM {campus.lower()}.{table.stem} 
                WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                AND layer in {cad_missing}"""
    cur.execute(sql_lines)
    conn.commit()


def import_dxf(campus, dxf_files, re_import=False):

    for dxf_file_name in dxf_files:

        dxf_file = get_dxf_fullpath(campus, dxf_file_name)

        floor = dxf_file.stem.split('_')[-3]

        if re_import:
            print(f"now droping table {dxf_file.stem}")
            sql_drop = F"DROP TABLE IF EXISTS {campus.lower()}.{dxf_file.stem} CASCADE"
            cur.execute(sql_drop)
            conn.commit()

            print("now removing old lines in db")
            sql_delete = F"DELETE FROM campuses.indrz_lines_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
            cur.execute(sql_delete)
            conn.commit()

            print("now removing old spaces in db")
            sql_delete_s = F"DELETE FROM campuses.indrz_spaces_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
            print(sql_delete_s)
            cur.execute(sql_delete_s)
            conn.commit()

        print(f"now running ogr to import dxf {dxf_file.stem}")
        dxf2postgis(dxf_file, campus)

        print(f"now inserting to lines and spaces into db  table called {dxf_file.stem}")
        insert_campuses_all(campus, dxf_file, lines=True, spaces=True)


def insert_all_dxf_files(campus):
    table_names = get_dxf_files(campus, floor=None, only_dxf_names=True)

    import_dxf(campus, table_names, re_import=True)


new_dxf_gusshaus = ['FA_FB_01_IP_042019.dxf',
                    'FA_FB_02_IP_042019.dxf',
                    'FA_FB_03_IP_042019.dxf',
                    'FA_FB_FC_EG_IP_042019.dxf',
                    'FA_FB_FC_U1_IP_042019.dxf',
                    'FA_FB_ZE_IP_042019.dxf',
                    'FB_04_IP_042019.dxf',
                    'FB_05_IP_042019.dxf',
                    'GA_01_IP_042019.dxf',
                    'GA_02_IP_042019.dxf',
                    'GA_07_DG_IP_042019.dxf',
                    'GA_EG_IP_042019.dxf',
                    'GA_U1_U2_IP_042019.dxf']

ch_new = ['CH_U1_IP_092018.dxf',
          'CH_03_IP_092018.dxf',
          'CH_02_IP_092018.dxf',
          'CH_EG_IP_092018.dxf',
          'CH_01_IP_092018.dxf']

new_karlsp_dxf = ['AA_AB_AC_AD_AE_AF_AG_AI_01_IP_112018.dxf',
                  'AA_AB_AC_AD_AE_AF_AG_AI_02_IP_112018.dxf',
                  'AA_AB_AC_AD_AE_AF_AG_AI_03_IP_112018.dxf',
                  'AA_AB_AC_AD_AE_AF_AG_AI_04_IP_112018.dxf',
                  'AA_AB_AC_AD_AE_AF_AG_AI_DG_IP_112018.dxf',
                  'AA_AB_AC_AD_AE_AF_AG_AI_EG_IP_112018.dxf',
                  'AA_AB_AC_AD_AE_AF_AG_AI_U1_IP_112018.dxf']

#import_dxf('Gusshaus', ch_new, re_import=True)

if __name__ == '__main__':
    # step1_import_all_dxf_to_working("Getreidemarkt")
    # step1_import_all_dxf_to_working("Gusshaus")
    # step1_import_all_dxf_to_working("Freihaus")
    # step1_import_all_dxf_to_working("Karlsplatz")  # 22.09.2019 22:44 done

    # step2_insert_lines_into_floor_tables("getreidemarkt")
    # step2_insert_lines_into_floor_tables("Gusshaus")
    # step2_insert_lines_into_floor_tables("Gusshaus")

    # step3_insert_spaces_into_floor_tables('Getreidemarkt')
    # step3_insert_spaces_into_floor_tables('Gusshaus')
    # step3_insert_spaces_into_floor_tables('Gusshaus')

    # insert_missing_cad_layer("Getreidemarkt", "bb", 'M_U29, M_Z29_NEU', remove=True)

    # import_dxf('Gusshaus', ['HK_EG_IP_082018.dxf',])
    # import_dxf('Getreidemarkt', ['PF_EG_IP_042019.dxf',], re_import=True)

    import_dxf('Getreidemarkt', ['BZ_02_IP_042019.dxf'])

    # drop_cad_table_reimport('Freihaus', ['DD_EG_IP_092018.dxf',])

    # import_dxf('Gusshaus', [])
    # import_dxf('Getreidemarkt', ['BI_05_IP_042019.dxf',], re_import=True)
    # import_dxf('Gusshaus', ['HK_EG_IP_082018.dxf',], re_import=True)
    # import_dxf('Gusshaus', ['HK_EG_IP_082018.dxf',])
    # import_dxf('Karlsplatz', new_karlsp_dxf)  # ran this on 22.09.2019  22:54

    # insert_all_dxf_files('Karlsplatz')
    # insert_all_dxf_files('Arsenal')
    # insert_all_dxf_files("Getreidemarkt", lines=True, spaces=True)
    # insert_all_dxf_files("Gusshaus", lines=True, spaces=True)
    # insert_all_dxf_files("Gusshaus", lines=True, spaces=True)




    conn.close()


# 2019.08.27 22:04
# ran this below
# 'DF_02_IP_092018.dxf' had many wrong layer names that need importing
# ['X_S_29', 'X_S27', 'X_O_F49', 'X_O_T49', 'X_H_L27', 'X_M_A29','X_M_Z29',]
# f = get_dxf_fullpath('Freihaus', 'DF_02_IP_092018.dxf')
# insert_missing_cadlines('Freihaus', f)


# drop_cad_table_reimport('Getreidemarkt', ['BI_EG_IP_042019.dxf',])

# TODO these I screwed up and need to be re-imported


# drop_cad_table_reimport('CA_CB_CC_CD_U1_IP_042019.dxf')
# drop_cad_table_reimport('Getreidemarkt', ['BI_EG_IP_042019.dxf', 'QA_EG_ZE_IP_15072019.dxf', 'BZ_EG_IP_042019.dwg'])
# drop_cad_table_reimport('Gusshaus',['CF_04_CG_06_IP_042019.dwg','CA_CB_CC_CD_U1_IP_042019.dwg'] )


# drop_cad_table_reimport('Freihaus', ['DA_DB_DC_07_IP_102018.dxf',
# 'DA_DB_DC_08_IP_102018.dxf',
# 'DD_04_IP_092018.dxf',
# 'DD_05_IP_092018.dxf',
# 'DD_EG_IP_092018.dxf',])




# subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", dxf_file.stem, str(dxf_file)])

# convert dxf to shapefile with polygon
# ogr2ogr -nlt polygon -skipfailures -f "ESRI Shapefile" shapeman4 ACAD-BIK_U2_IP_042019.dxf
#ogr2ogr -nlt polygon -sql "SELECT Layer from entities where Layer='Z_009'" -skipfailures -f "ESRI Shapefile" shapeman11 ACAD-BIK_U2_IP_042019.dxf

#ogr2ogr -nlt point -sql "SELECT Layer from entities where Layer='XRnr'" -skipfailures -f "ESRI Shapefile" shapeman15 ACAD-BIK_U2_IP_042019.dxf

# ogr2ogr -gcp -gcp <ungeoref_x> <ungeoref_y> <georef_x> <georef_y> <elevation>
#You can do this in PostGIS using ST_Affine
#ST_Rotate for PostGIS 2.0.
#https://gis.stackexchange.com/questions/21696/rotating-a-vector-layer-in-qgis-with-qgsaffine-or-other-method
# qgis translate function for georeferencing
# qgis rotate function


# import ogr

# driver = ogr.GetDriverByName('DXF')
# datasource = driver.Open('test1.dxf', 0)

# layers=datasource.ExecuteSQL( "SELECT DISTINCT Layer FROM entities" )
# layer=datasource.GetLayerByIndex(0)

# for i in range(0, layers.GetFeatureCount()):
#         layerName = layers.GetFeature(i).GetFieldAsString(0)
#         layer.SetAttributeFilter( "Layer='%s'" % layerName)
#         print 'Layer=%s|Features=%s' % (layerName, layer.GetFeatureCount())


# print(len([name for name, group in grouped]))

# for name, group in grouped:
#     print(group)
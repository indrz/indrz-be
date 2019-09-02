import pandas as pd
from pandas.compat import StringIO, BytesIO
import os
from pathlib import Path, PurePath

import subprocess
import psycopg2


con_string = "dbname=" + os.getenv('DB_NAME') + " user=" + os.getenv('DB_USER') + " host=" + os.getenv('DB_HOST') + " password=" + os.getenv('DB_PASSWORD')

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


unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO', 'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']

def floor_map():
    unique_floor_name_map = []
    for f in unique_floor_names:
        value = ""
        if f == "DG":
            value = "Dachgeschoß"
        elif f == "EG":
            value = "Erdgeschoß"
        elif f == "SO":
            value = "Souterrain"
        elif f.startswith("U"):
            value = "Untergeschoß"
        elif f.startswith("Z"):
            value = "Zwischengeschoß"
        else:
            value = "Obergeschoß"
        
        d = dict(value, f)
        unique_floor_name_map.append(d)

    return floor_map

floor_names_odd = ['ZD', 'ZE', 'ZU','DG', 'EG', 'SO']
floor_names_u = ['U1', 'U2', 'U3', 'U4']
floor_names_z = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']
floor_names_int = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


def get_floor_int(name):
    if not name:
        return name
    floor = name.stem.split("_")[-3]

    if floor in floor_names_odd:
        if floor == "EG":
            floor = 0
        else:
            floor = 9999

    if floor in floor_names_z:
        # zwischen stock
        floor = floor[1] + 1000
    
    if floor in floor_names_int:
        floor = int(floor)
    
    if floor in floor_names_u:
        # underground
        floor = int(floor[1]) * -1

    return floor


# TRAKTS
#Karlsplatz ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AP', 'AQ', 'AS', 'AT', 'EA', 'EB', 'EC']
#Getreidemarkt ['BA', 'BB', 'BC', 'BD', 'BE', 'BG', 'BH', 'BI', 'BK', 'BL', 'BZ', 'PF', 'QA']
#Gusshaus ['CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'FA', 'FB', 'FC', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HK', 'HL']
#Freihaus ['DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'ZA', 'ZB', 'ZC', 'ZD']
#Arsenal ['MA', 'MB', 'MC', 'MD', 'MG', 'MH', 'MI', 'OA', 'OB', 'OC', 'OY', 'OZ']
#Ausweichquartier ['WA', 'WB', 'WC', 'WD']

def read_campus_csv_list():
    df = pd.read_csv('gebauede-tu-juli-2019.csv', names=["CAMPUS","TRAKT","TRAKTBEZEICHNUNG","ADRESSE","PLZ","ORT","GESCHOSS"], delimiter=";")
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
                            x = t.groupby('TRAKT')
                            tt = [name for name, group in x]
                            print("address ", a, " tracks at this address ", tt)

# read_campus_csv_list()

def get_dxf_fullpath(campus, dxf_file_name):
    dxf_dir_path = Path('c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/' + campus + '/dxf')

    dxf_file_full_path = Path.joinpath(dxf_dir_path, dxf_file_name)

    return dxf_file_full_path


def get_dxf_files(campus_name, floor=None):

    dxf_dir_path = Path('c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/' + campus_name + '/dxf')
    dxf_list = os.listdir(dxf_dir_path)
    dxf_files = []
    for dxf in dxf_list:
        if PurePath(dxf).suffix == ".dxf":
                dxf_files.append(dxf)
    #print(len(dxf_files))

    dxf_file_paths = []

    for dxf in dxf_files:
        p = Path.joinpath(dxf_dir_path, dxf)
        if floor:
            if p.stem.split('_')[1] == floor:
                dxf_file_paths.append(p)
        else:
            dxf_file_paths.append(p)

    return dxf_file_paths

def dxf2postgis(dxf_file, campus_name):
    
    floor_names = set()
    track_names = set()

    line_table_names = []
    space_table_names = []
    lable_table_names = []
        
    dxf_floor = dxf_file.stem.split('_')[-3]
    floor_names.add(dxf_floor)
    track_names.add(dxf_file.stem.split('_')[0])

    dxf_file_name = dxf_file.stem

    # import linestrings
    # line_table_name = "indrz_lines_" + str(dxf_floor)
    table_name = str(dxf_file.stem)
    line_table_names.append(dxf_file.stem)

    sql_linestrings = "SELECT Layer from entities where Layer in {0}".format(cad_layer_names)
    print(f"now running table {table_name}")

    subprocess.run([
        "ogr2ogr", "-a_srs", "EPSG:31259", "-oo", "DXF_FEATURE_LIMIT_PER_BLOCK=-1", 
        "-nlt", "PROMOTE_TO_MULTI", "-oo", "DXF_INLINE_BLOCKS=FALSE", "-oo", "DXF_MERGE_BLOCK_GEOMETRIES=False", 
        "-lco", f"SCHEMA={campus_name.lower()}", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", table_name, str(dxf_file)])

    #--config DXF_INLINE_BLOCKS FALSE --config DXF_MERGE_BLOCK_GEOMETRIES FALSE
    #subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-sql", sql_linestrings, "-lco", f"SCHEMA={campus_name.lower()}", "-lco", "DXF_FEATURE_LIMIT_PER_BLOCK=-1", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", line_table_name, str(dxf_file)])
    # subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-sql", sql_linestrings, "-lco", f"SCHEMA={campus_name.lower()}", "-lco", "DXF_FEATURE_LIMIT_PER_BLOCK=-1", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", line_table_name, str(dxf_file),"-append", "-update",])
    #subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-sql", sql_linestrings, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, str(dxf_file), "-nln", line_table_name])
    
    # import spaces
    space_table_name = "indrz_spaces_" + str(dxf_floor)
    space_table_names.append(space_table_name)
    sql_spaces = "SELECT Layer from entities where Layer='Z_009'"
    #subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-nlt", "POLYGON", "-sql", sql_spaces, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", space_table_name, str(dxf_file)])
    #subprocess.run(["ogr2ogr", "-update", "-append", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-nlt", "POLYGON", "-sql", sql_spaces, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", space_table_name, str(dxf_file)])

    # import txt points
    text_table_name = "indrz_text_" + str(dxf_floor)
    lable_table_names.append(text_table_name)
    sql_text = "SELECT Layer from entities where Layer in ('B_127N', 'B_227Z')"
    #subprocess.run(["ogr2ogr", "-update", "-append", "-a_srs", "EPSG:31259", "-nlt", "POINT", "-sql", sql_text, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, "-dsco", "DXF_INLINE_BLOCKS=False", "-nln", text_table_name, str(dxf_file)])


            #print("running dxf file ", str(dxf_file))
    # print("floor nums , ", sorted(floor_names))
    # print("trackt names : ", sorted(track_names))
            #DXF_INLINE_BLOCKS

            # "-nlt", "MULTILINESTRING",
                #ogr2ogr -f "PostgreSQL" PG:"host=localhost user=indrztu dbname=indrztudata password=air" -nlt GEOMETRY ACAD-BIK_U2_IP_042019.dxf
                # ogr2ogr -update -append -fieldmap -1,-1,2 -a_srs EPSG:900913 -nlt MULTILINESTRING -lco "SCHEMA=geodata" -f PostgreSQL "PG:host=localhost port=5432 user=postgres dbname=mydb password=secret" -nln geodata.table_name shapefileName.shp



def dxf_to_postgis_old(dxf_file_name, campus):

    dxf_dir_path = Path('c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/' + campus + '/dxf')

    dxf_filepath = Path.joinpath(dxf_dir_path, dxf_file_name)

    
    floor = dxf_filepath.stem.split('_')[1]
# "-sql", sql_linestrings, 
    # sql_linestrings = "SELECT Layer from entities where Layer in {0}".format(cad_layer_names)
    subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-oo", "DXF_FEATURE_LIMIT_PER_BLOCK=-1", 
    "-nlt", "PROMOTE_TO_MULTI", 
    "-oo", "DXF_INLINE_BLOCKS=FALSE", "-oo", "DXF_MERGE_BLOCK_GEOMETRIES=False", "-lco", f"SCHEMA={campus.lower()}", 
    "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", dxf_filepath.stem, str(dxf_filepath)])

    # floor = dxf_file.stem.split('_')[1]
    
    # dest_table_name = f"indrz_lines_{floor}"

    # sql = f"""INSERT INTO {campus}.{dest_table_name}(long_name, geom) SELECT layer, wkb_geometry 
    #             FROM {campus}.indrz_lines_{table.stem} 
    #             WHERE GeometryType(wkb_geometry)='MULTILINESTRING'"""
    # print(sql)
    # cur.execute(sql)
    # conn.commit()

#dxf_to_postgis("BB_01_IP_042019.dxf", "Getreidemarkt")


def step1_import_all_dxf_to_working(campus):
    dxf_file_paths = get_dxf_files(campus)
    for dxf_file in dxf_file_paths:
        dxf2postgis(dxf_file, campus)

# step1_import_all_dxf_to_working("Getreidemarkt")
# step1_import_all_dxf_to_working("Gusshaus")
# step1_import_all_dxf_to_working("Freihaus")

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


# step2_insert_lines_into_floor_tables("getreidemarkt")
# step2_insert_lines_into_floor_tables("Gusshaus")

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

#step3_insert_spaces_into_floor_tables('Getreidemarkt')
#step3_insert_spaces_into_floor_tables('Gusshaus')

def insert_missing_cad_layer(campus, trak, cad_layer_name, remove=False,insert=False):
    """ select data from a specific cad layer and insert into our db """

    table_names = get_dxf_files("Getreidemarkt")

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
# insert_missing_cad_layer("Getreidemarkt", "bb", 'M_U29, M_Z29_NEU', remove=True)

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


def insert_campuses(campus, lines=False, spaces=False):

    table_names = get_dxf_files(campus)

    for table in table_names:
        insert_campuses_all(campus, table, lines=True, spaces=Trued)
        #insert_missing_cadlines(campus, table)

# insert_campuses("Getreidemarkt", lines=True, spaces=True)
# insert_campuses("Gusshaus", lines=True, spaces=True)
# insert_campuses("Gusshaus", lines=True, spaces=True)


def drop_cad_table_reimport(campus, dxf_files):

    for dxf_file_name in dxf_files:
        
        dxf_file = get_dxf_fullpath(campus, dxf_file_name)

        floor = dxf_file.stem.split('_')[-3]

        # print(f"now droping table {dxf_file.stem}")
        # sql_drop = F"DROP TABLE IF EXISTS {campus.lower()}.{dxf_file.stem} CASCADE"
        # cur.execute(sql_drop)
        # conn.commit()

        # sql_delete = F"DELETE FROM campuses.indrz_lines_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
        # cur.execute(sql_drop)
        # conn.commit()

        # sql_delete_s = F"DELETE FROM campuses.indrz_spaces_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
        # print(sql_delete_s)
        # cur.execute(sql_delete_s)
        # conn.commit()

        print(f"now re-importing dxf {dxf_file.stem}")
        dxf2postgis(dxf_file, campus)

        print(f"now inserting to lines and spaces table {dxf_file.stem}")
        insert_campuses_all(campus, dxf_file, lines=True, spaces=True)

drop_cad_table_reimport('Freihaus', ['DD_EG_IP_092018.dxf',])
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

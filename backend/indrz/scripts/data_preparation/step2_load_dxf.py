import subprocess
import psycopg2
from pathlib import Path
from utils import ogr_db_con, con_dj_string, get_dxf_files, get_dxf_fullpath

conn = psycopg2.connect(con_dj_string)
cur = conn.cursor()

from setup_campus import cad_linestring_layers, cad_spaces_layers, cad_umriss_layers, cad_layers_outdoor_ply


def dxf2postgis(dxf_file):
    f = Path(dxf_file)
    print("my path to f", f)
    table_name = str(f.stem)

    # subprocess.run([
    #     "ogr2ogr", "-a_srs", "EPSG:31259",
    #     "-nlt", "PROMOTE_TO_MULTI",
    #     "-lco", "OVERWRITE=YES",
    #     "-lco", f"SCHEMA={campus_name.lower()}", "-skipfailures", "-f", "PostgreSQL", ogr_db_con_navigatur,
    #     "-nln", table_name.lower(), str(dxf_file)])

    subprocess.run([
        "ogr2ogr", "-a_srs", "EPSG:31259", "-dim", "2",
        "-oo", "DXF_FEATURE_LIMIT_PER_BLOCK=-1",
        "-nlt", "PROMOTE_TO_MULTI",
        "-oo", "DXF_INLINE_BLOCKS=FALSE",
        "-oo", "DXF_MERGE_BLOCK_GEOMETRIES=False",
        "-lco", f"SCHEMA=dxf_tables",
        "-skipfailures", "-f", "PostgreSQL", ogr_db_con, "-nln", table_name.lower(), str(dxf_file)])

    print("DONE running ogr2ogr")

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

        sql = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) 
                    SELECT layer, ARRAY['{table.stem}', layer], wkb_geometry 
                    FROM {campus.lower()}.{table.stem} 
                    WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                    AND layer in {cad_linestring_layers}"""
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

        sql = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) 
                    SELECT layer, ARRAY['{table.stem}', layer], 
                    st_multi(st_buildarea(st_forceclosed(wkb_geometry)))
                    FROM {campus.lower()}.{table.stem} 
                    WHERE ST_NPoints(wkb_geometry) >= 4
                    AND ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                    AND layer in ('{cad_spaces_layers}')"""
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
                sql = f"""INSERT INTO {campus}.{dest_table_name}(long_name, geom) 
                        SELECT layer, wkb_geometry 
                            FROM {campus}.{table.stem} 
                            WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                            AND layer in ('{cad_layer_name}')"""
            print(sql)

            cur.execute(sql)
            conn.commit()


def insert_campuses_lines_spaces(campus, table):
    floor = table.stem.split('_')[-3]

    print(f"inserting LINES {table.stem}")
    dest_table_name = f"indrz_lines_{floor}"
    sql_lines = f"""INSERT INTO campuses.{dest_table_name} (long_name, tags, geom) 
            SELECT layer, ARRAY['{table.stem}', layer], wkb_geometry 
                FROM {campus.lower()}.{table.stem} 
                WHERE ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                AND layer in {cad_linestring_layers}"""
    cur.execute(sql_lines)
    conn.commit()

    print(f"inserting SPACES {table.stem}")
    dest_table_name = f"indrz_spaces_{floor}"
    sql_spaces = f"""INSERT INTO campuses.{dest_table_name}(long_name, tags, geom) 
            SELECT layer, ARRAY['{table.stem}', layer], 
            st_multi(st_makepolygon(st_linemerge(st_forceclosed(wkb_geometry))))
            -- st_multi(st_buildarea(st_forceclosed(wkb_geometry)))
                FROM {campus.lower()}.{table.stem} 
                WHERE ST_NPoints(wkb_geometry) >= 4
                AND ST_GeometryType(wkb_geometry)='ST_MultiLineString'
                AND layer in ('{cad_spaces_layers}')"""
    cur.execute(sql_spaces)
    conn.commit()



def import_dxf(campus, dxf_files, re_import=False):

    for dxf_file_name in dxf_files:

        dxf_file = get_dxf_fullpath(campus, dxf_file_name)

        floor = dxf_file.stem.split('_')[-3]

        if re_import:
            # print(f" DROPPING table {dxf_file.stem}")
            sql_drop = F"DROP TABLE IF EXISTS {campus.lower()}.{dxf_file.stem} CASCADE"
            cur.execute(sql_drop)
            conn.commit()

            print(f" DELETING old lines in db for {dxf_file.stem}")
            sql_delete = F"DELETE FROM campuses.indrz_lines_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
            cur.execute(sql_delete)
            conn.commit()

            print(f" DELETING old spaces in db for {dxf_file.stem}")
            sql_delete_s = F"DELETE FROM campuses.indrz_spaces_{floor} CASCADE WHERE tags[1] = '{dxf_file.stem}'"
            cur.execute(sql_delete_s)
            conn.commit()

        # print(f"---- now running ogr to import dxf {dxf_file.stem}")
        # dxf2postgis(dxf_file, campus)
        #
        # print(f"---- now inserting to lines and spaces into db  table called {dxf_file.stem}")
        # insert_campuses_lines_spaces(campus, dxf_file)
        #
        # print(f"---- now importing UMRISS for dxf {dxf_file.stem}")
        # insert_umriss(campus, dxf_file)


def insert_all_dxf_files(campus):
    table_names = get_dxf_files(campus, floor=None, only_dxf_names=True)

    import_dxf(campus, table_names, re_import=True)



if __name__ == '__main__':

    conn.close()

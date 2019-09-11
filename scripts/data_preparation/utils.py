from pathlib import Path
import subprocess
import os
import psycopg2


db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
db_connection = f"PG: host={db_host} user={db_user} dbname={db_name} password={db_pass}"

conn = psycopg2.connect(con_string)
cur = conn.cursor()



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


# dxf_to_postgis("BB_01_IP_042019.dxf", "Getreidemarkt")

# sql_linestrings = "SELECT Layer from entities where Layer in {0}".format(cad_layer_names)
# print(f"now running table {table_name}")

# --config DXF_INLINE_BLOCKS FALSE --config DXF_MERGE_BLOCK_GEOMETRIES FALSE
# subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-sql", sql_linestrings, "-lco", f"SCHEMA={campus_name.lower()}", "-lco", "DXF_FEATURE_LIMIT_PER_BLOCK=-1", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", line_table_name, str(dxf_file)])
# subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-sql", sql_linestrings, "-lco", f"SCHEMA={campus_name.lower()}", "-lco", "DXF_FEATURE_LIMIT_PER_BLOCK=-1", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", line_table_name, str(dxf_file),"-append", "-update",])
# subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-sql", sql_linestrings, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, str(dxf_file), "-nln", line_table_name])

# import spaces
space_table_name = "indrz_spaces_" + str(dxf_floor)
space_table_names.append(space_table_name)
sql_spaces = "SELECT Layer from entities where Layer='Z_009'"
# subprocess.run(["ogr2ogr", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-nlt", "POLYGON", "-sql", sql_spaces, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", space_table_name, str(dxf_file)])
# subprocess.run(["ogr2ogr", "-update", "-append", "-a_srs", "EPSG:31259", "-nlt", "PROMOTE_TO_MULTI", "-nlt", "POLYGON", "-sql", sql_spaces, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, "-nln", space_table_name, str(dxf_file)])

# import txt points
text_table_name = "indrz_text_" + str(dxf_floor)
lable_table_names.append(text_table_name)
sql_text = "SELECT Layer from entities where Layer in ('B_127N', 'B_227Z')"
# subprocess.run(["ogr2ogr", "-update", "-append", "-a_srs", "EPSG:31259", "-nlt", "POINT", "-sql", sql_text, "-lco", "SCHEMA=geodata", "-skipfailures", "-f", "PostgreSQL", db_connection, "-dsco", "DXF_INLINE_BLOCKS=False", "-nln", text_table_name, str(dxf_file)])


# print("running dxf file ", str(dxf_file))
# print("floor nums , ", sorted(floor_names))
# print("trackt names : ", sorted(track_names))
# DXF_INLINE_BLOCKS

# "-nlt", "MULTILINESTRING",
# ogr2ogr -f "PostgreSQL" PG:"host=localhost user=indrztu dbname=indrztudata password=air" -nlt GEOMETRY ACAD-BIK_U2_IP_042019.dxf
# ogr2ogr -update -append -fieldmap -1,-1,2 -a_srs EPSG:900913 -nlt MULTILINESTRING -lco "SCHEMA=geodata" -f PostgreSQL "db -nln geodata.table_name shapefileName.shp


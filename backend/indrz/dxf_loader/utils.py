import subprocess
from pathlib import Path
from typing import List
from .config import PG_DSN
from django.db import connection

def copy_table_with_prefix(original_table_name, prefix="tst_"):
    new_table_name = f"{prefix}{original_table_name}"
    with connection.cursor() as cursor:
        # Create the new table with the same structure
        cursor.execute(f"CREATE TABLE dxf_original.{new_table_name} (LIKE dxf_original.{original_table_name} INCLUDING ALL);")

        cursor.execute(f"""SELECT AddGeometryColumn ('dxf_original','{new_table_name}','geom',3857,'POINT',2);""")
        # Copy the data
        cursor.execute(f"INSERT INTO dxf_original.{new_table_name} SELECT * FROM dxf_original.{original_table_name};")

# -------------- ogr2ogr wrapper ------------------
def ogr2ogr_import(file: Path, table_name: str):
    print(f"Running ogr2ogr Importing {file} to {table_name}")
    cmd: List[str] = [
        "ogr2ogr",
        "-dim", "2",
        "-a_srs", "EPSG:3857",
        "-oo", "DXF_FEATURE_LIMIT_PER_BLOCK=-1",
        "-oo", "DXF_INLINE_BLOCKS=FALSE",
        "-oo", "DXF_MERGE_BLOCK_GEOMETRIES=False",
        "-nlt", "PROMOTE_TO_MULTI",
        "-lco", "SCHEMA=dxf_original",
        "-skipfailures",
        "-f", "PostgreSQL", f"PG: {PG_DSN}",
        str(file),
        "-lco", "FID=gid",
        "-lco", "GEOMETRY_NAME=geom",
        "-nln", table_name
    ]
    subprocess.check_call(cmd)

# def ogr2ogr_import(file: Path, table_name: str):
#     print(f"Running ogr2ogr Importing {file} to {table_name}")
#     cmd: List[str] = [
#         "ogr2ogr",
#         "-dim", "2",
#         "-oo", "DXF_FEATURE_LIMIT_PER_BLOCK=-1",
#         "-oo", "DXF_INLINE_BLOCKS=FALSE",
#         "-oo", "DXF_MERGE_BLOCK_GEOMETRIES=False",
#         "-nlt", "PROMOTE_TO_MULTI",
#         "-lco", "SCHEMA=dxf_original",
#         "-skipfailures",
#         "-f", "PostgreSQL", f"PG: {PG_DSN}",
#         str(file),
#         "-lco", "FID=gid",
#         "-lco", "GEOMETRY_NAME=geom",
#         "-nln", table_name,
#         "-overwrite"
#     ]
#     subprocess.check_call(cmd)